from rest_framework import viewsets
from accounts.permissions import IsParent
from attendance.models import Attendance, BehaviorLog
from attendance.serializers.parent import ParentAttendanceSerializer, ParentBehaviorLogSerializer

class ParentAttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    """Parents can view their child's attendance records."""
    serializer_class = ParentAttendanceSerializer
    permission_classes = [IsParent]

    def get_queryset(self):
        return Attendance.objects.filter(student__parents__user=self.request.user).order_by("-date")


class ParentBehaviorLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Parents can view their child's behavior logs."""
    serializer_class = ParentBehaviorLogSerializer
    permission_classes = [IsParent]

    def get_queryset(self):
        return BehaviorLog.objects.filter(student__parents__user=self.request.user).order_by("-date")
