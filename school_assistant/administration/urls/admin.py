from django.urls import path

from administration.views.admin import (
    ComplaintViewSet, InventoryViewSet, InventorySummaryView, SchoolEventViewSet,
    EventParticipationViewSet, CertificateViewSet, CertificateGenerateView, CertificateDownloadView,
)

urlpatterns = [
    path("support/complaints", ComplaintViewSet.as_view({"get": "list", "post": "create"})),
    path("support/complaints/<int:pk>", ComplaintViewSet.as_view({"get": "retrieve"})),
    path("support/complaints/<int:pk>/status", ComplaintViewSet.as_view({"put": "partial_update"})),

    path("admin/inventory", InventoryViewSet.as_view({"get": "list", "post": "create"})),
    path("admin/inventory/<int:pk>", InventoryViewSet.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
    )),
    path("admin/inventory/summary", InventorySummaryView.as_view()),

    path("admin/events", SchoolEventViewSet.as_view({"get": "list", "post": "create"})),
    path("admin/events/<int:pk>", SchoolEventViewSet.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
    )),
    path("events/upcoming", SchoolEventViewSet.as_view({"get": "list"})),

    path("admin/events/<int:event_id>/participants", EventParticipationViewSet.as_view({"get": "list", "post": "create"})),

    path("admin/certificates/generate", CertificateGenerateView.as_view()),
    path("admin/certificates", CertificateViewSet.as_view({"get": "list"})),
    path("admin/certificates/<int:pk>", CertificateViewSet.as_view({"get": "retrieve"})),
    path("admin/certificates/<int:id>/download", CertificateDownloadView.as_view()),
]