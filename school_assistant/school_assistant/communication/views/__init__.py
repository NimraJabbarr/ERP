# communication/views/__init__.py

from .admin import (
    NotificationListView, UnreadNotificationListView,
    MarkNotificationReadView, MarkAllNotificationsReadView,
    MediaCampaignViewSet, PublishCampaignView, CampaignLogListView,
)

from .student import StudentNotificationListView
from .teacher import TeacherNotificationListView
from .parent import ParentNotificationListView
