"""
ATTENDANCE -- ADMIN-ROLE VIEWS
=================================
"""

from django.db.models import Count, Q
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.models import Attendance, BehaviorLog
from accounts.permissions import IsAdmin
from attendance.serializers.admin import AttendanceRecordSerializer, BehaviorLogSerializer


class AttendanceSummaryView(APIView):
    """
    GET /api/attendance/summary
    Feeds the Admin Dashboard's attendance trend chart (Page 5). Returns
    a simple live aggregation -- no separate caching table needed at this
    data scale (see earlier discussion on aggregation tables).
    """
    permission_classes = [IsAdmin]

    def get(self, request):
        date = request.query_params.get("date")
        qs = Attendance.objects.all()
        if date:
            qs = qs.filter(date=date)

        totals = qs.aggregate(
            present=Count("id", filter=Q(status="Present")),
            absent=Count("id", filter=Q(status="Absent")),
            leave=Count("id", filter=Q(status="Leave")),
        )
        return Response(totals)


class BehaviorLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Admin overview of all behavior logs, filterable by severity
    (?severity=High) for the Behavior Log Overview screen.
    """
    serializer_class = BehaviorLogSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        qs = BehaviorLog.objects.select_related("student__user", "reported_by__user").all()
        severity = self.request.query_params.get("severity")
        if severity:
            qs = qs.filter(severity=severity)
        return qs