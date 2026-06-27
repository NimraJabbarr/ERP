from rest_framework import serializers
from communication.models import Notification

class TeacherNotificationSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.full_name", read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "sender_name", "type", "message", "is_read", "created_at"]
        read_only_fields = ["sender_name", "created_at"]
