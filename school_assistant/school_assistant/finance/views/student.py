from rest_framework import viewsets
from accounts.permissions import IsStudent
from finance.models import Fee, Payment
from finance.serializers.student import StudentFeeSerializer, StudentPaymentSerializer

class StudentFeeViewSet(viewsets.ReadOnlyModelViewSet):
    """Students can view their own fee invoices."""
    serializer_class = StudentFeeSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Fee.objects.filter(student__user=self.request.user).order_by("-month")


class StudentPaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """Students can view their own payment history."""
    serializer_class = StudentPaymentSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Payment.objects.filter(fee__student__user=self.request.user).order_by("-payment_date")
