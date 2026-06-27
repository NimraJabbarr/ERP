from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError

from accounts.permissions import IsTeacher
from academics.models import Subject
from attendance.models import Attendance, BehaviorLog
from attendance.serializers.teacher import (
    TeacherAttendanceSerializer,
    TeacherBehaviorLogSerializer,
)


class TeacherAttendanceViewSet(viewsets.ModelViewSet):
    """Teachers can mark and update attendance for their class."""

    serializer_class = TeacherAttendanceSerializer
    permission_classes = [IsTeacher]

    def get_queryset(self):
        # Teachers can only see/update the attendance records they have marked.
        return Attendance.objects.filter(marked_by=self.request.user.teacher_profile)









    def _assert_not_locked(self, obj: Attendance):

        if getattr(obj, "is_locked", False):
            raise ValidationError(
                "Attendance record is locked for this day and cannot be modified."
            )


    def perform_create(self, serializer):
        teacher_profile = self.request.user.teacher_profile

        # Teacher scoping: teacher can only mark attendance for students in class-sections they teach.
        student = serializer.validated_data.get("student")
        class_section = serializer.validated_data.get("class_section")

        if not student or not class_section:
            raise ValidationError({"detail": "student and class_section are required."})

        if getattr(student, "class_section_id", None) != class_section.id:
            raise PermissionDenied("Invalid class_section for the provided student.")

        has_subject_for_section = Subject.objects.filter(
            assigned_teacher=teacher_profile,
            class_section=class_section,
        ).exists()
        if not has_subject_for_section:
            raise PermissionDenied("You are not assigned to this class-section.")

        # If some client sends is_locked=True, still ensure new records are unlocked.
        serializer.save(marked_by=teacher_profile, is_locked=False)

    def perform_update(self, serializer):
        self._assert_not_locked(self.get_object())
        serializer.save()

    def perform_destroy(self, instance: Attendance):
        self._assert_not_locked(instance)
        instance.delete()


class TeacherBehaviorLogViewSet(viewsets.ModelViewSet):
    """Teachers can file behavior logs for students."""

    serializer_class = TeacherBehaviorLogSerializer
    permission_classes = [IsTeacher]

    def get_queryset(self):
        # restrict to logs filed by this teacher
        return BehaviorLog.objects.filter(reported_by=self.request.user.teacher_profile)

    def perform_create(self, serializer):
        teacher_profile = self.request.user.teacher_profile

        student = serializer.validated_data.get("student")
        if not student:
            raise ValidationError({"detail": "student is required."})

        # Teacher scoping: teacher can only log behavior for students in sections they teach.
        class_section_id = getattr(student, "class_section_id", None)
        if not class_section_id:
            raise PermissionDenied("Student has no class_section assigned.")

        has_subject_for_section = Subject.objects.filter(
            assigned_teacher=teacher_profile,
            class_section_id=class_section_id,
        ).exists()
        if not has_subject_for_section:
            raise PermissionDenied("You are not assigned to this student's class-section.")

        serializer.save(reported_by=teacher_profile)

