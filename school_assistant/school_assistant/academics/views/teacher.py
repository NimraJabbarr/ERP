from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError

from accounts.permissions import IsTeacher
from academics.models import Grade, Assignment, AssignmentSubmission, Subject

from academics.serializers.teacher import (
    TeacherGradeEntrySerializer,
    TeacherAssignmentSerializer,
    TeacherAssignmentSubmissionSerializer,
)


class TeacherGradeViewSet(viewsets.ModelViewSet):
    """CRUD /api/teacher/grades"""

    serializer_class = TeacherGradeEntrySerializer
    permission_classes = [IsTeacher]

    def get_queryset(self):
        # restrict to grades entered by this teacher
        return Grade.objects.filter(teacher__user=self.request.user)

    def perform_create(self, serializer):
        teacher_profile = self.request.user.teacher_profile

        # Teacher scoping: teacher can only create grades for subjects assigned to them.
        student = serializer.validated_data.get("student")
        subject = serializer.validated_data.get("subject")

        if not student or not subject:
            raise ValidationError({"detail": "student and subject are required."})

        if subject.assigned_teacher_id != teacher_profile.id:
            raise PermissionDenied("You are not assigned as the teacher for this subject.")

        # Ensure the student belongs to the same class-section as the subject.
        if getattr(student, "class_section_id", None) != subject.class_section_id:
            raise PermissionDenied("You cannot enter grades for a student not in this subject's class-section.")

        serializer.save(teacher=teacher_profile)


class TeacherAssignmentViewSet(viewsets.ModelViewSet):
    """CRUD /api/teacher/assignments"""

    serializer_class = TeacherAssignmentSerializer
    permission_classes = [IsTeacher]

    def get_queryset(self):
        # restrict to assignments created by this teacher
        return Assignment.objects.filter(teacher__user=self.request.user)

    def perform_create(self, serializer):
        teacher_profile = self.request.user.teacher_profile

        # Teacher scoping: teacher can only create assignments for subjects
        # assigned to them.
        subject = serializer.validated_data.get("subject")
        class_section = serializer.validated_data.get("class_section")

        if not subject or not class_section:
            raise ValidationError({"detail": "subject and class_section are required."})

        # subject-ownership check (same logic as TeacherGradeViewSet)
        if subject.assigned_teacher_id != teacher_profile.id:
            raise PermissionDenied("You are not assigned as the teacher for this subject.")

        if subject.class_section_id != class_section.id:
            raise PermissionDenied("class_section does not match this subject.")

        serializer.save(teacher=teacher_profile)




class TeacherSubmissionViewSet(viewsets.ModelViewSet):
    """CRUD /api/teacher/submissions"""

    serializer_class = TeacherAssignmentSubmissionSerializer
    permission_classes = [IsTeacher]

    def get_queryset(self):
        # restrict to submissions for assignments owned by this teacher
        return AssignmentSubmission.objects.filter(assignment__teacher__user=self.request.user)

