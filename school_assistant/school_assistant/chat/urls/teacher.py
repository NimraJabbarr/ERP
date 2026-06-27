from django.urls import path
from chat.views.teacher import TeacherChatSessionViewSet, TeacherChatMessageViewSet

urlpatterns = [
    path("teacher/chat/sessions", TeacherChatSessionViewSet.as_view({"get": "list", "post": "create"})),
    path("teacher/chat/sessions/<int:pk>", TeacherChatSessionViewSet.as_view({"get": "retrieve"})),

    path("teacher/chat/messages", TeacherChatMessageViewSet.as_view({"get": "list", "post": "create"})),
    path("teacher/chat/messages/<int:pk>", TeacherChatMessageViewSet.as_view({"get": "retrieve"})),
]
