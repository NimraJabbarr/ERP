from django.urls import path
from attendance.views.student import StudentAttendanceViewSet, StudentBehaviorLogViewSet

urlpatterns = [
    path("student/attendance", StudentAttendanceViewSet.as_view({"get": "list"})),
    path("student/attendance/<int:pk>", StudentAttendanceViewSet.as_view({"get": "retrieve"})),

    path("student/behavior-logs", StudentBehaviorLogViewSet.as_view({"get": "list"})),
    path("student/behavior-logs/<int:pk>", StudentBehaviorLogViewSet.as_view({"get": "retrieve"})),
]
