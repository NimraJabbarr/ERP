from django.urls import path
from communication.views.student import StudentNotificationListView

urlpatterns = [
    path("student/notifications", StudentNotificationListView.as_view()),
]
