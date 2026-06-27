"""
Project-level URL configuration.

This file should only need one new line per app, ever -- the actual,
frequent route additions happen inside each app's own
urls/admin.py / teacher.py / student.py / parent.py.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="School ERP API",
        default_version="v1",
        description="REST API for the Smart School ERP (Admin / Teacher / Student / Parent)",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Renamed from /admin/ to /admin-site/ so it doesn't clash with our
    # own /api/admin/... route prefix used for the Admin role's endpoints.
    path("admin-site/", admin.site.urls),

    # Swagger / ReDoc -- visit /swagger/ for interactive API testing.
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    path("api/", include("accounts.urls")),
    path("api/", include("academics.urls")),
    path("api/", include("attendance.urls")),
    path("api/", include("finance.urls")),
    path("api/", include("communication.urls")),
    path("api/", include("administration.urls")),
    path("api/", include("chat.urls")), 
]