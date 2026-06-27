from django.urls import path

from chat.views.admin import ChatSessionListCreateView, ChatSessionDeleteView, ChatMessageListView

urlpatterns = [
    path("chat/sessions", ChatSessionListCreateView.as_view()),
    path("chat/sessions/<int:session_id>", ChatSessionDeleteView.as_view()),
    path("chat/messages/<int:session_id>", ChatMessageListView.as_view()),
]