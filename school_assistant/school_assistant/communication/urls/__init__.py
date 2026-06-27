from django.urls import path, include

urlpatterns = [
    path("", include("communication.urls.admin")),
    path("", include("communication.urls.student")),
    path("", include("communication.urls.teacher")),
    path("", include("communication.urls.parent")),
]