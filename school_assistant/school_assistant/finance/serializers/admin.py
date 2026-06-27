"""
FINANCE -- ADMIN-ROLE SERIALIZERS
====================================
"""

from rest_framework import serializers

from finance.models import FeeStructure, Fee, Payment, Expense, FeeHistory


class FeeStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeStructure
        fields = ["id", "class_section", "monthly_fee", "created_at", "updated_at"]


class FeeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.full_name", read_only=True)

    class Meta:
        model = Fee
        fields = [
            "id", "student", "student_name", "fee_structure", "month",
            "original_amount", "amount", "amount_paid", "due_date",
            "paid_date", "status", "generated_at",
        ]
        read_only_fields = ["amount_paid", "status", "generated_at"]  # kept in sync by Payment, not edited directly


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "fee", "amount_paid", "payment_method", "transaction_id", "payment_date", "created_at"]
        read_only_fields = ["created_at"]


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            "id", "category", "description", "amount", "expense_date",
            "paid_by_admin", "payment_method", "created_at",
        ]
        read_only_fields = ["paid_by_admin", "created_at"]


class FeeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeHistory
        fields = [
            "id", "fee", "old_status", "new_status", "old_amount",
            "new_amount", "changed_by_admin", "reason", "created_at",
        ]