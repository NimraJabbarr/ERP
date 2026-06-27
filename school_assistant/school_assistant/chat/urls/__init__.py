from django.urls import path, include

urlpatterns = [
    path("", include("chat.urls.admin")),

    path("", include("chat.urls.student")),
    path("", include("chat.urls.teacher")),

    path("", include("chat.urls.parent")),





]