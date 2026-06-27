from django.urls import path
from accounts.views.student import StudentViewSet

# Explicit mapping to avoid DRF DefaultRouter auto-generating unintended routes.
# This app exposes CRUD-like endpoints only for explicitly listed methods.
urlpatterns = [
    # Collection (must include all methods in a single route; otherwise DRF returns 405)
    path(
        "students",
        StudentViewSet.as_view({"get": "list", "post": "create"}),
        name="student-list-create",
    ),

    # Detail

    path(
        "students/<int:pk>",
        StudentViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
        }),
        name="student-detail",
    ),

    # Intentionally omit "delete" to prevent unintended DELETE exposure.
]






