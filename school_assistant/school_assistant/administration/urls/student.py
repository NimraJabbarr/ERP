from django.urls import path
from administration.views.student import (
    StudentComplaintViewSet, StudentEventParticipationViewSet, StudentCertificateViewSet
)

urlpatterns = [
    path("student/complaints", StudentComplaintViewSet.as_view({"get": "list", "post": "create"})),
    path("student/complaints/<int:pk>", StudentComplaintViewSet.as_view({"get": "retrieve"})),

    path("student/events/participations", StudentEventParticipationViewSet.as_view({"get": "list"})),
    path("student/events/participations/<int:pk>", StudentEventParticipationViewSet.as_view({"get": "retrieve"})),

    path("student/certificates", StudentCertificateViewSet.as_view({"get": "list"})),
    path("student/certificates/<int:pk>", StudentCertificateViewSet.as_view({"get": "retrieve"})),
]
