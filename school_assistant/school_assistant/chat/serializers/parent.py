from rest_framework import serializers
from chat.models import ChatSession, ChatMessage

class ParentChatSessionSerializer(serializers.ModelSerializer):
    active_child_name = serializers.CharField(source="active_child.user.full_name", read_only=True)

    class Meta:
        model = ChatSession
        fields = ["id", "bot_type", "title", "active_child", "active_child_name", "created_at"]


class ParentChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ["id", "role", "content", "created_at"]
