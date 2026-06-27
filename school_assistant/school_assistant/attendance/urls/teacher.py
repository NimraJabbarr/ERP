from django.urls import path
from attendance.views.teacher import TeacherAttendanceViewSet, TeacherBehaviorLogViewSet

urlpatterns = [
    path("teacher/attendance", TeacherAttendanceViewSet.as_view({"get": "list", "post": "create"})),
    path("teacher/attendance/<int:pk>", TeacherAttendanceViewSet.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update"}
    )),

    path("teacher/behavior-logs", TeacherBehaviorLogViewSet.as_view({"get": "list", "post": "create"})),
    path("teacher/behavior-logs/<int:pk>", TeacherBehaviorLogViewSet.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update"}
    )),
]
