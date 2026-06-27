from rest_framework import serializers
from finance.models import Fee, Payment

class StudentFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fee
        fields = ["id", "month", "original_amount", "amount", "amount_paid", "due_date", "paid_date", "status"]
        read_only_fields = ["amount_paid", "status", "paid_date"]


class StudentPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "fee", "amount_paid", "payment_method", "transaction_id", "payment_date"]
        read_only_fields = ["payment_date"]
