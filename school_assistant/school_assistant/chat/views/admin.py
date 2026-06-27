"""
CHAT -- SHARED VIEWS (every role uses these)
================================================
Session/message CRUD only -- see the module docstring in serializers/admin.py
for what's deliberately NOT here (the actual AI reply + WebSocket layer).
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from chat.models import ChatSession, ChatMessage
from chat.serializers.admin import ChatSessionSerializer, ChatMessageSerializer


class ChatSessionListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/chat/sessions  -- sidebar history, scoped to the logged-in user
    POST /api/chat/sessions  -- start a new conversation (or pick a bot, if Admin)
    """
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChatSessionDeleteView(generics.DestroyAPIView):
    """DELETE /api/chat/sessions/{session_id}"""
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "session_id"

    def get_queryset(self):
        # Scoped to the logged-in user so nobody can delete someone else's session.
        return ChatSession.objects.filter(user=self.request.user)


class ChatMessageListView(generics.ListAPIView):
    """GET /api/chat/messages/{session_id} -- full message history for one conversation."""
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ownership check: only return messages if the session belongs to
        # the requesting user (404s naturally via filter -- no leakage).
        return ChatMessage.objects.filter(
            session_id=self.kwargs["session_id"], session__user=self.request.user
        )