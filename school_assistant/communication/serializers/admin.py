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

    #  VALIDATION: Message minimum 5 characters
    def validate_message(self, value):
        if not value or len(value.strip()) < 5:
            raise serializers.ValidationError("Message must be at least 5 characters long.")
        return value.strip()


class MediaCampaignLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaCampaignLog
        fields = [
            "id", "post_content", "post_type", "platform",
            "status", "created_by_admin", "created_at",
        ]
        read_only_fields = ["status", "created_by_admin", "created_at"]

    # VALIDATION: Sirf facebook/linkedin/instgram allow hain
    def validate_platform(self, value):
        ALLOWED = ['facebook', 'linkedin','instagram',]
        if value not in ALLOWED:
            raise serializers.ValidationError(
                f"Invalid platform. Allowed: {', '.join(ALLOWED)}"
            )
        return value