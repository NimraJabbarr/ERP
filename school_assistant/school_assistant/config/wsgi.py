"""
WSGI config. Used for plain HTTP deployment (e.g. on Render/Vercel) where
WebSocket support isn't required by the deployment target.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
