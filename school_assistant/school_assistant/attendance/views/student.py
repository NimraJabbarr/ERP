from rest_framework import viewsets
from accounts.permissions import IsStudent
from attendance.models import Attendance, BehaviorLog
from attendance.serializers.student import StudentAttendanceSerializer, StudentBehaviorLogSerializer

class StudentAttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    """Students can view their own attendance records."""
    serializer_class = StudentAttendanceSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Attendance.objects.filter(student__user=self.request.user).order_by("-date")


class StudentBehaviorLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Students can view their own behavior logs."""
    serializer_class = StudentBehaviorLogSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return BehaviorLog.objects.filter(student__user=self.request.user).order_by("-date")
