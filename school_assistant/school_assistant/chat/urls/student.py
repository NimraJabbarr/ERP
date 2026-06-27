from django.urls import path
from chat.views.student import StudentChatSessionViewSet, StudentChatMessageViewSet

urlpatterns = [
    path("student/chat/sessions", StudentChatSessionViewSet.as_view({"get": "list", "post": "create"})),
    path("student/chat/sessions/<int:pk>", StudentChatSessionViewSet.as_view({"get": "retrieve"})),

    path("student/chat/messages", StudentChatMessageViewSet.as_view({"get": "list", "post": "create"})),
    path("student/chat/messages/<int:pk>", StudentChatMessageViewSet.as_view({"get": "retrieve"})),
]
