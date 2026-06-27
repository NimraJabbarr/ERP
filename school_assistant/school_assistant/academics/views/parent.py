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
        # Parent should only see grades for students linked to this parent.
        return (
            Grade.objects.select_related("subject", "student")
            .filter(student__parent_links__parent__user=self.request.user)
        )


class ParentSubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/parent/submissions"""

    serializer_class = ParentAssignmentSubmissionSerializer
    permission_classes = [IsAdminOrParent]

    def get_queryset(self):
        # Parent should only see submissions for students linked to this parent.
        return (
            AssignmentSubmission.objects.select_related(
                "assignment", "student"
            )
            .filter(student__parent_links__parent__user=self.request.user)
        )

