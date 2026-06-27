"""
ASGI config.

Required because the AI chatbot uses WebSockets (via Django Channels) for
real-time message delivery, in addition to normal HTTP request/response.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# This must be created BEFORE importing anything that touches models, so
# Django's app registry is ready first.
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # TODO: add chat.routing.websocket_urlpatterns here once
            # chat/consumers.py and chat/routing.py are built, e.g.:
            # path("ws/chat/<int:session_id>/", ChatConsumer.as_asgi()),
        ])
    ),
})
