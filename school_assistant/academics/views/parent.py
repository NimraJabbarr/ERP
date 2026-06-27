from rest_framework import viewsets

from accounts.permissions import IsAdminOrParent

from academics.models import AssignmentSubmission, Grade
from academics.serializers.parent import (
    ParentAssignmentSubmissionSerializer,
    ParentGradeSerializer,
)


class ParentGradeViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/parent/grades"""

    serializer_class = ParentGradeSerializer
    permission_classes = [IsAdminOrParent]

    def get_queryset(self):
        # Admin can view all; parent can view only their linked students.
        from accounts.permissions import is_admin_user

        if is_admin_user(self.request):
            return Grade.objects.select_related("subject", "student")

        return (
            Grade.objects.select_related("subject", "student")
            .filter(student__parent_links__parent__user=self.request.user)
        )



class ParentSubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/parent/submissions"""

    serializer_class = ParentAssignmentSubmissionSerializer
    permission_classes = [IsAdminOrParent]

    def get_queryset(self):
        # Admin can view all; parent can view only their linked students.
        from accounts.permissions import is_admin_user

        if is_admin_user(self.request):
            return AssignmentSubmission.objects.select_related("assignment", "student")

        return (
            AssignmentSubmission.objects.select_related("assignment", "student")
            .filter(student__parent_links__parent__user=self.request.user)
        )


