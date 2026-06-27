from django.urls import path, include

urlpatterns = [
    path("", include("administration.urls.admin")),
    path("", include("administration.urls.student")),
    path("", include("administration.urls.teacher")),
    path("", include("administration.urls.parent")),
]