from django.urls import path
from communication.views.parent import ParentNotificationListView

urlpatterns = [
    path("parent/notifications", ParentNotificationListView.as_view()),
]
