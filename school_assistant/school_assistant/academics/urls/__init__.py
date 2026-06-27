from django.urls import path, include

urlpatterns = [
    path("", include("academics.urls.admin")),
    # academics.urls.teacher -- Grades/Assignments routes, built by Dev B
    path("", include("academics.urls.student")),
    path("", include("academics.urls.teacher")),
    path("", include("academics.urls.parent")),
]