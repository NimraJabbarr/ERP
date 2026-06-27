from django.urls import path

from communication.views.admin import (
    NotificationListView, UnreadNotificationListView, MarkNotificationReadView,
    MarkAllNotificationsReadView, MediaCampaignViewSet, PublishCampaignView, CampaignLogListView,
)

urlpatterns = [
    path("support/notifications", NotificationListView.as_view()),
    path("notifications/unread", UnreadNotificationListView.as_view()),
    path("notifications/read/<int:id>", MarkNotificationReadView.as_view()),
    path("notifications/read-all", MarkAllNotificationsReadView.as_view()),

    path("admin/campaigns", MediaCampaignViewSet.as_view({"get": "list", "post": "create"})),
    path("admin/campaigns/publish", PublishCampaignView.as_view()),
    path("admin/campaigns/logs", CampaignLogListView.as_view()),
]