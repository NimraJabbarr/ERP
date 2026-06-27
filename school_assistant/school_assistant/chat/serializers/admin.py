"""
CHAT -- SHARED SERIALIZERS (used by every role)
==================================================
Session/message CRUD is identical for every role -- only the actual AI
reply (planned separately, over WebSocket) differs by bot_type and
role-based data scoping. This file covers the "traditional" REST parts
only: creating/listing/deleting sessions, and listing messages.
"""

from rest_framework import serializers

from chat.models import ChatSession, ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ["id", "session", "role", "content", "created_at"]
        read_only_fields = ["created_at"]


class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ["id", "user", "bot_type", "title", "active_child", "created_at"]
        read_only_fields = ["id", "user", "created_at"]

    def validate_bot_type(self, value):
        # Per spec: only Admin gets the 10-bot "Bot Hub" (Maintenance,
        # Fee, Media, etc.). Teacher/Student/Parent each get one scoped
        # "general" assistant -- they cannot pick a specialized bot.
        request = self.context["request"]
        if request.user.role.role_name != "Admin" and value != "general":
            raise serializers.ValidationError(
                "Only Admin can select a specialized bot. Other roles use the general assistant."
            )
        return value

    def validate_active_child(self, value):
        # active_child only makes sense for Parent sessions (the
        # dashboard's child-toggle). Block it from being set by anyone else.
        request = self.context["request"]
        if value is not None and request.user.role.role_name != "Parent":
            raise serializers.ValidationError("Only Parent sessions can be scoped to a child.")
        return value