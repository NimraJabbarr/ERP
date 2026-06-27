"""
COMMUNICATION -- ADMIN-ROLE SERIALIZERS
==========================================
"""

from rest_framework import serializers

from communication.models import Notification, MediaCampaignLog


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id", "sender", "receiver", "type", "message",
            "reference_type", "reference_id", "is_read", "created_at",
        ]
        read_only_fields = ["created_at"]


class MediaCampaignLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaCampaignLog
        fields = [
            "id", "post_content", "post_type", "platform",
            "status", "created_by_admin", "created_at",
        ]
        read_only_fields = ["status", "created_by_admin", "created_at"]