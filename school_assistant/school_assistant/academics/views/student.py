from rest_framework import viewsets
from accounts.permissions import IsStudent
from academics.models import Grade, Assignment, AssignmentSubmission
from academics.serializers.student import (
    GradeSerializer, AssignmentSerializer, AssignmentSubmissionSerializer
)

class StudentGradeViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/student/grades"""
    serializer_class = GradeSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        # restrict to logged-in student only
        return Grade.objects.filter(student__user=self.request.user)


class StudentAssignmentViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/student/assignments"""
    serializer_class = AssignmentSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        # restrict to assignments of student's class
        student_profile = self.request.user.student_profile
        return Assignment.objects.filter(class_section_id=student_profile.class_section_id)


class StudentSubmissionViewSet(viewsets.ModelViewSet):
    """CRUD /api/student/submissions"""
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        # restrict to submissions of logged-in student
        return AssignmentSubmission.objects.filter(student__user=self.request.user)

    def perform_create(self, serializer):
        student_profile = self.request.user.student_profile
        assignment = serializer.validated_data["assignment"]
        if assignment.class_section_id != student_profile.class_section_id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("This assignment is not assigned to your class.")
        serializer.save(student=student_profile)
