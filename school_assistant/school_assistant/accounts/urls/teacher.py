from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views.teacher import TeacherViewSet

router = DefaultRouter()
router.register(r'teachers', TeacherViewSet, basename="teachers")

urlpatterns = [
    path("", include(router.urls)),
]
