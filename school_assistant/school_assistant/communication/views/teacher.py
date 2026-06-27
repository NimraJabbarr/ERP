from rest_framework import generics
from accounts.permissions import IsTeacher
from communication.models import Notification
from communication.serializers.teacher import TeacherNotificationSerializer

class TeacherNotificationListView(generics.ListAPIView):
    """Teachers can view their own notifications."""
    serializer_class = TeacherNotificationSerializer
    permission_classes = [IsTeacher]

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user).order_by("-created_at")
