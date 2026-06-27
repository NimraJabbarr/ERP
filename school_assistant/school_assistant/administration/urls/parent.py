from django.urls import path
from administration.views.parent import (
    ParentComplaintViewSet, ParentEventParticipationViewSet, ParentCertificateViewSet
)

urlpatterns = [
    path("parent/complaints", ParentComplaintViewSet.as_view({"get": "list", "post": "create"})),
    path("parent/complaints/<int:pk>", ParentComplaintViewSet.as_view({"get": "retrieve"})),

    path("parent/events/participations", ParentEventParticipationViewSet.as_view({"get": "list"})),
    path("parent/events/participations/<int:pk>", ParentEventParticipationViewSet.as_view({"get": "retrieve"})),

    path("parent/certificates", ParentCertificateViewSet.as_view({"get": "list"})),
    path("parent/certificates/<int:pk>", ParentCertificateViewSet.as_view({"get": "retrieve"})),
]
