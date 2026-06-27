from rest_framework import serializers
from chat.models import ChatSession, ChatMessage

class StudentChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ["id", "bot_type", "title", "created_at"]


class StudentChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ["id", "role", "content", "created_at"]
