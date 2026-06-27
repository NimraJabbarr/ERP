from django.urls import path

from attendance.views.admin import AttendanceSummaryView, BehaviorLogViewSet

urlpatterns = [
    path("attendance/summary", AttendanceSummaryView.as_view()),
    path("admin/behavior-logs", BehaviorLogViewSet.as_view({"get": "list"})),
    path("admin/behavior-logs/<int:pk>", BehaviorLogViewSet.as_view({"get": "retrieve"})),
]