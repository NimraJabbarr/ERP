from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from accounts.permissions import IsTeacher
from chat.models import ChatSession, ChatMessage
from chat.serializers.teacher import TeacherChatSessionSerializer, TeacherChatMessageSerializer

class TeacherChatSessionViewSet(viewsets.ModelViewSet):
    """Teachers can create and view their own chat sessions."""
    serializer_class = TeacherChatSessionSerializer
    permission_classes = [IsTeacher]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, bot_type="general")


class TeacherChatMessageViewSet(viewsets.ModelViewSet):
    """Teachers can send and view messages in their sessions."""
    serializer_class = TeacherChatMessageSerializer
    permission_classes = [IsTeacher]

    def get_queryset(self):
        return ChatMessage.objects.filter(session__user=self.request.user).order_by("created_at")

    def perform_create(self, serializer):
        session_id = self.request.data.get("session")
        if not session_id:
            raise ValidationError({"session": "This field is required."})

        # IDOR fix: ensure the session belongs to this authenticated teacher.
        session = get_object_or_404(ChatSession, id=session_id, user=self.request.user)
        serializer.save(session=session, role="user")

