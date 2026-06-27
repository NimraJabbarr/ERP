from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views.parent import ParentViewSet, ParentStudentLinkViewSet

router = DefaultRouter()
router.register(r'parents', ParentViewSet, basename="parents")
router.register(r'parent-links', ParentStudentLinkViewSet, basename="parent-links")

urlpatterns = [
    path("", include(router.urls)),
]
