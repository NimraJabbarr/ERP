from rest_framework import viewsets
from accounts.permissions import IsParent
from finance.models import Fee, Payment
from finance.serializers.parent import ParentFeeSerializer, ParentPaymentSerializer

class ParentFeeViewSet(viewsets.ReadOnlyModelViewSet):
    """Parents can view their child's fee invoices."""
    serializer_class = ParentFeeSerializer
    permission_classes = [IsParent]

    def get_queryset(self):
        return Fee.objects.filter(student__parents__user=self.request.user).order_by("-month")


class ParentPaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """Parents can view their child's payment history."""
    serializer_class = ParentPaymentSerializer
    permission_classes = [IsParent]

    def get_queryset(self):
        return Payment.objects.filter(fee__student__parents__user=self.request.user).order_by("-payment_date")
