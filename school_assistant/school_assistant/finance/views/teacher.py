from rest_framework import viewsets
from accounts.permissions import IsTeacher
from finance.models import Expense
from finance.serializers.teacher import TeacherExpenseSerializer

class TeacherExpenseViewSet(viewsets.ModelViewSet):
    """Teachers can log and view expenses (e.g. classroom supplies)."""
    serializer_class = TeacherExpenseSerializer
    permission_classes = [IsTeacher]

    def get_queryset(self):
        return Expense.objects.filter(paid_by_admin=self.request.user).order_by("-expense_date")

    def perform_create(self, serializer):
        serializer.save(paid_by_admin=self.request.user)
