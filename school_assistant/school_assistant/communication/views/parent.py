from rest_framework import generics
from accounts.permissions import IsParent
from communication.models import Notification
from communication.serializers.parent import ParentNotificationSerializer

class ParentNotificationListView(generics.ListAPIView):
    """Parents can view their own notifications (including child-related ones)."""
    serializer_class = ParentNotificationSerializer
    permission_classes = [IsParent]

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user).order_by("-created_at")
