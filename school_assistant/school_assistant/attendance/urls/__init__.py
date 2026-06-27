from django.urls import path, include

urlpatterns = [
    path("", include("attendance.urls.admin")),
    # attendance.urls.teacher -- mark/lock attendance + file behavior logs, built by Dev B
    path("", include("attendance.urls.student")),
    path("", include("attendance.urls.teacher")),
    path("", include("attendance.urls.parent")),
]