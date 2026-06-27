from django.urls import path
from chat.views.parent import ParentChatSessionViewSet, ParentChatMessageViewSet

urlpatterns = [
    path("parent/chat/sessions", ParentChatSessionViewSet.as_view({"get": "list", "post": "create"})),
    path("parent/chat/sessions/<int:pk>", ParentChatSessionViewSet.as_view({"get": "retrieve"})),

    path("parent/chat/messages", ParentChatMessageViewSet.as_view({"get": "list", "post": "create"})),
    path("parent/chat/messages/<int:pk>", ParentChatMessageViewSet.as_view({"get": "retrieve"})),
]
