"""
Project-level URL configuration.

This file is meant to stay almost frozen after initial setup -- once each
app's own urls.py exists (built later, alongside views/serializers), add
ONE line per app here, e.g.:

    path("api/", include("accounts.urls")),
    path("api/", include("academics.urls")),

Keeping this file untouched day-to-day is what lets two developers work
on different role-scoped endpoints in parallel without merge conflicts --
each app's own urls/admin.py, urls/others.py, etc. is where the real,
frequent route additions happen.
"""

from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="School ERP API",
        default_version="v1",
        description="REST API for the Smart School ERP system (Admin / Teacher / Student / Parent).",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Swagger UI -- interactive API testing straight from the browser.
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    # ReDoc -- clean, read-only API reference (nice for sharing with the team).
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    # TODO: add one line per app once its own urls.py exists, e.g.:
    # path("api/", include("accounts.urls")),
    # path("api/", include("academics.urls")),
    # path("api/", include("attendance.urls")),
    # path("api/", include("finance.urls")),
    # path("api/", include("chat.urls")),
    # path("api/", include("communication.urls")),
    # path("api/", include("administration.urls")),
]
