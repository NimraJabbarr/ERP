from rest_framework import serializers
from finance.models import Fee, Payment

class ParentFeeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.full_name", read_only=True)

    class Meta:
        model = Fee
        fields = [
            "id", "student_name", "month", "original_amount", "amount",
            "amount_paid", "due_date", "paid_date", "status"
        ]
        read_only_fields = ["student_name", "amount_paid", "status", "paid_date"]


class ParentPaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="fee.student.user.full_name", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id", "fee", "student_name", "amount_paid",
            "payment_method", "transaction_id", "payment_date"
        ]
        read_only_fields = ["student_name", "payment_date"]
