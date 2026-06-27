from rest_framework import serializers
from finance.models import Expense

class TeacherExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ["id", "category", "description", "amount", "expense_date", "payment_method"]
