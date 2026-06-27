from django.urls import path
from communication.views.teacher import TeacherNotificationListView

urlpatterns = [
    path("teacher/notifications", TeacherNotificationListView.as_view()),
]
