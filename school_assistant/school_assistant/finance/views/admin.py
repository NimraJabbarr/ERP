"""
FINANCE -- ADMIN-ROLE VIEWS
==============================
Includes Stripe online payments. Stripe is a payment GATEWAY, unrelated
to the AI/chatbot work -- it belongs here in the traditional system.
"""

import logging
from decimal import Decimal

import stripe
from django.conf import settings
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import StudentProfile
from accounts.permissions import IsAdmin
from finance.models import FeeStructure, Fee, Payment, Expense, FeeHistory
from finance.serializers.admin import (
    FeeStructureSerializer, FeeSerializer, PaymentSerializer, ExpenseSerializer, FeeHistorySerializer,
)

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY


# ── SHARED HELPER ─────────────────────────────────────────────────────────
def sync_fee_after_payment(fee, payment, changed_by_admin=None, reason=""):
    """
    Single source of truth for keeping Fee.amount_paid/status in sync
    with the Payment ledger, and logging the change to FeeHistory.

    Used by BOTH the manual PaymentCreateView (Admin recording Cash/Bank
    Transfer) and the Stripe webhook below (online card payments) --
    extracted here so the two payment paths can never drift out of sync
    with each other.
    """
    old_status = fee.status
    total_paid = fee.payments.aggregate(total=Sum("amount_paid"))["total"] or Decimal(0)
    fee.amount_paid = total_paid
    fee.status = "Paid" if total_paid >= fee.amount else ("Partial" if total_paid > 0 else "Unpaid")
    if fee.status == "Paid":
        fee.paid_date = payment.payment_date
    fee.save()

    if old_status != fee.status:
        FeeHistory.objects.create(
            fee=fee, old_status=old_status, new_status=fee.status,
            old_amount=fee.amount, new_amount=fee.amount,
            changed_by_admin=changed_by_admin, reason=reason or f"Payment of {payment.amount_paid} recorded.",
        )


class FeeStructureViewSet(viewsets.ModelViewSet):
    queryset = FeeStructure.objects.select_related("class_section").all()
    serializer_class = FeeStructureSerializer
    permission_classes = [IsAdmin]


class FeeViewSet(viewsets.ModelViewSet):
    """
    CRUD /api/finance/challans
    Fee.amount_paid/status are read-only here -- they only change through
    PaymentCreateView/StripeWebhookView below (both call sync_fee_after_payment).
    """
    queryset = Fee.objects.select_related("student__user", "fee_structure").all()
    serializer_class = FeeSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        fee = serializer.save()
        FeeHistory.objects.create(
            fee=fee, new_status=fee.status, new_amount=fee.amount,
            changed_by_admin=self.request.user, reason="Challan manually created by Admin.",
        )

    def perform_update(self, serializer):
        old_fee = self.get_object()
        old_status, old_amount = old_fee.status, old_fee.amount
        fee = serializer.save()
        if old_status != fee.status or old_amount != fee.amount:
            FeeHistory.objects.create(
                fee=fee, old_status=old_status, new_status=fee.status,
                old_amount=old_amount, new_amount=fee.amount,
                changed_by_admin=self.request.user, reason="Challan manually corrected by Admin.",
            )


class GenerateMonthlyChallansView(APIView):
    """
    POST /api/finance/generate-monthly-challans
    Manual trigger for the same logic the Celery cron job runs
    automatically at the start of each month. Fetches each student's
    class fee, applies their scholarship discount, and creates a Fee row
    -- skips students who already have one for that month.
    """
    permission_classes = [IsAdmin]

    def post(self, request):
        month = request.data.get("month")  # expected format: "YYYY-MM-01"
        if not month:
            return Response({"month": "Required, e.g. 2026-07-01"}, status=400)

        created_count, skipped_count = 0, 0

        for student in StudentProfile.objects.select_related("class_section").all():
            fee_structure = FeeStructure.objects.filter(class_section=student.class_section).first()
            if not fee_structure:
                continue

            if Fee.objects.filter(student=student, month=month).exists():
                skipped_count += 1
                continue

            discount = Decimal(student.scholarship_percentage) / Decimal(100)
            original_amount = fee_structure.monthly_fee
            amount = original_amount * (Decimal(1) - discount)

            Fee.objects.create(
                student=student, fee_structure=fee_structure, month=month,
                original_amount=original_amount, amount=amount,
                due_date=month, status="Unpaid",
            )
            created_count += 1

        return Response({"created": created_count, "skipped_existing": skipped_count})


class PaymentCreateView(generics.CreateAPIView):
    """
    POST /api/finance/payments
    Manual payment entry -- for Cash/Bank Transfer that Admin records
    after physically receiving it. Online/Card payments go through the
    Stripe flow below instead, NOT through this endpoint.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        payment = serializer.save()
        sync_fee_after_payment(payment.fee, payment, changed_by_admin=self.request.user)


class PaymentListView(generics.ListAPIView):
    """GET /api/finance/payments/{fee_id}"""
    serializer_class = PaymentSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return Payment.objects.filter(fee_id=self.kwargs["fee_id"]).order_by("-payment_date")


class ExpenseViewSet(viewsets.ModelViewSet):
    """CRUD /api/admin/expenses"""
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        serializer.save(paid_by_admin=self.request.user)


class FeeHistoryListView(generics.ListAPIView):
    """GET /api/finance/fee-history/{fee_id}"""
    serializer_class = FeeHistorySerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return FeeHistory.objects.filter(fee_id=self.kwargs["fee_id"]).order_by("-created_at")


# ── STRIPE ONLINE PAYMENTS ──────────────────────────────────────────────

class CreateStripePaymentIntentView(APIView):
    """
    POST /api/finance/stripe/create-payment-intent
    Body: {"fee_id": 1}

    Creates a Stripe PaymentIntent for the remaining balance on a Fee and
    returns its client_secret. The frontend uses Stripe.js/Stripe Elements
    with that client_secret to actually collect the card and confirm
    payment -- this endpoint never touches card details directly (PCI
    compliance: card data should never pass through our own server).

    IMPORTANT: this does NOT mark anything as paid. Only a verified
    webhook event from Stripe (below) ever creates a Payment row -- never
    trust a "payment succeeded" claim coming from the frontend alone,
    since that could be spoofed by a malicious client.
    """
    permission_classes = [IsAdmin]  # Admin generates the payment link for now; Dev B can reuse this for a Parent-facing "pay now" button later

    def post(self, request):
        fee = get_object_or_404(Fee, id=request.data.get("fee_id"))
        remaining = fee.amount - fee.amount_paid

        if remaining <= 0:
            return Response({"detail": "This fee is already fully paid."}, status=400)

        try:
            intent = stripe.PaymentIntent.create(
                amount=int(remaining * 100),  # Stripe expects the smallest currency unit (e.g. paisa)
                currency="pkr",
                metadata={"fee_id": str(fee.id), "student_id": str(fee.student_id)},
            )
        except stripe.error.StripeError as exc:
            logger.error("Stripe PaymentIntent creation failed: %s", exc)
            return Response({"detail": "Could not start payment. Please try again."}, status=502)

        return Response({"client_secret": intent.client_secret, "amount_due": str(remaining)})


class StripeWebhookView(APIView):
    """
    POST /api/finance/stripe/webhook
    Called BY STRIPE's servers, never by the frontend or Postman directly.

    Security: every request's signature is verified against
    STRIPE_WEBHOOK_SECRET before any data is trusted -- this is what
    proves the request genuinely came from Stripe and wasn't forged by
    someone hitting this URL directly to fake a payment.
    """
    permission_classes = [AllowAny]   # Stripe cannot send a JWT -- trust comes from the signature check below instead
    authentication_classes = []        # skip DRF auth entirely for this endpoint

    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        except (ValueError, stripe.error.SignatureVerificationError) as exc:
            logger.warning("Rejected Stripe webhook with invalid signature: %s", exc)
            return Response(status=400)

        if event["type"] == "payment_intent.succeeded":
            intent = event["data"]["object"]

            # Idempotency: Stripe may deliver the same event more than
            # once -- never double-credit a payment.
            if Payment.objects.filter(stripe_payment_intent_id=intent["id"]).exists():
                return Response(status=200)

            fee_id = intent["metadata"]["fee_id"]  # StripeObject doesn't support .get() in this SDK version -- bracket access only
            fee = get_object_or_404(Fee, id=fee_id)
            amount_paid = Decimal(intent["amount_received"]) / Decimal(100)

            payment = Payment.objects.create(
                fee=fee, amount_paid=amount_paid, payment_method="Online",
                stripe_payment_intent_id=intent["id"], payment_date=timezone.now().date(),
            )
            sync_fee_after_payment(fee, payment, changed_by_admin=None, reason="Paid online via Stripe.")

        return Response(status=200)