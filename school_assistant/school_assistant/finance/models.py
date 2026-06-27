"""
FINANCE APP
===========
Fee structures, monthly fee challans, the payment transaction ledger,
school expenses, and a fee-change audit trail.

Cross-app references used in this file:
- FeeStructure.class_section -> academics.ClassSection
- Fee.student -> accounts.StudentProfile
- Expense.paid_by_admin, FeeHistory.changed_by_admin -> accounts.User
"""

from django.db import models


class FeeStructure(models.Model):
    """Defines the monthly fee amount for a given class."""

    class_section = models.ForeignKey(
        "academics.ClassSection", on_delete=models.CASCADE, related_name="fee_structures"
    )
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Fee(models.Model):
    """A single month's fee challan/invoice for one student."""

    STATUS_CHOICES = (("Paid", "Paid"), ("Unpaid", "Unpaid"), ("Partial", "Partial"))

    student = models.ForeignKey("accounts.StudentProfile", on_delete=models.CASCADE, related_name="fees")
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.PROTECT, related_name="fees")

    # Stored as the 1st day of the month (e.g. 2026-06-01) -- easier to
    # sort/filter in queries and in the Celery cron job than a free-text
    # value like "June 2026".
    month = models.DateField(db_index=True)

    original_amount = models.DecimalField(max_digits=10, decimal_places=2)  # before scholarship discount
    amount = models.DecimalField(max_digits=10, decimal_places=2)           # payable, after discount applied

    # Cached running total for fast dashboard reads. The Payment model
    # below is the actual transaction ledger -- this field is kept in
    # sync (incremented) whenever a new Payment row is created.
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Unpaid", db_index=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "month")  # one challan per student per month


class Payment(models.Model):
    """
    The actual payment transaction ledger. Every individual payment
    (full or partial) against a Fee gets its own row here -- this is
    what makes the "Partial" status meaningful and auditable, instead
    of relying on a single overwritable field.
    """

    METHOD_CHOICES = (
        ("Cash", "Cash"), ("Card", "Card"), ("Bank Transfer", "Bank Transfer"), ("Online", "Online"),
    )

    fee = models.ForeignKey(Fee, on_delete=models.CASCADE, related_name="payments")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES)

    # Stripe idempotency / traceability. This field was added in migration
    # 0002 but was missing from the model class, which crashes the webhook.
    stripe_payment_intent_id = models.CharField(
        max_length=255, blank=True, null=True, unique=True
    )

    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    # NOTE: application logic (or a post_save signal) should re-sum all
    # Payments for this Fee into Fee.amount_paid, and update Fee.status
    # accordingly (Unpaid -> Partial -> Paid).



class Expense(models.Model):
    """School operating expenses -- electricity, salaries, maintenance, etc."""

    CATEGORY_CHOICES = (
        ("Electricity", "Electricity"), ("Salaries", "Salaries"),
        ("Furniture", "Furniture"), ("Maintenance", "Maintenance"), ("Other", "Other"),
    )

    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateField()
    paid_by_admin = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, related_name="expenses_logged"
    )
    payment_method = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class FeeHistory(models.Model):
    """Audit trail: logs every status/amount change made to a Fee row."""

    fee = models.ForeignKey(Fee, on_delete=models.CASCADE, related_name="history")
    old_status = models.CharField(max_length=10, blank=True)
    new_status = models.CharField(max_length=10, blank=True)
    old_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    new_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    changed_by_admin = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, related_name="fee_changes_made"
    )
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
