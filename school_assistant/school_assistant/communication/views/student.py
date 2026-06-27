from rest_framework import generics
from accounts.permissions import IsStudent
from communication.models import Notification
from communication.serializers.student import StudentNotificationSerializer

class StudentNotificationListView(generics.ListAPIView):
    """Students can view their own notifications."""
    serializer_class = StudentNotificationSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user).order_by("-created_at")
