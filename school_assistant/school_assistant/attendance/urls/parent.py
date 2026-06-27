from django.urls import path
from attendance.views.parent import ParentAttendanceViewSet, ParentBehaviorLogViewSet

urlpatterns = [
    path("parent/attendance", ParentAttendanceViewSet.as_view({"get": "list"})),
    path("parent/attendance/<int:pk>", ParentAttendanceViewSet.as_view({"get": "retrieve"})),

    path("parent/behavior-logs", ParentBehaviorLogViewSet.as_view({"get": "list"})),
    path("parent/behavior-logs/<int:pk>", ParentBehaviorLogViewSet.as_view({"get": "retrieve"})),
]
