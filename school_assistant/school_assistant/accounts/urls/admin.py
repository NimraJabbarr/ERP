"""
ACCOUNTS -- ADMIN-ROLE URLS
=============================
Includes both the shared auth endpoints (used by every role) and the
admin-exclusive management endpoints. Teacher/Student/Parent url files
do NOT redefine register/login/profile/change-password -- they are
registered once, here, since the underlying view logic is identical for
every role (see the note in serializers/admin.py for why).
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from accounts.views.admin import (
    RegisterView, ProfileView, ChangePasswordView,
    PasswordResetRequestView, PasswordResetConfirmView,
    RoleListView, PendingApprovalListView, ApprovalActionView,
    UserViewSet, StudentProfileViewSet, TeacherProfileViewSet,
)

urlpatterns = [
    # ── Shared auth (every role) ────────────────────────────────────────
    path("auth/register", RegisterView.as_view(), name="auth-register"),
    path("auth/login", TokenObtainPairView.as_view(), name="auth-login"),

    path("auth/login/refresh", TokenRefreshView.as_view(), name="auth-login-refresh"),
    path("auth/profile", ProfileView.as_view(), name="auth-profile"),
    path("auth/change-password", ChangePasswordView.as_view(), name="auth-change-password"),
    path("auth/password-reset", PasswordResetRequestView.as_view(), name="auth-password-reset"),
    path("auth/password-reset/confirm", PasswordResetConfirmView.as_view(), name="auth-password-reset-confirm"),

    # ── Admin-only ───────────────────────────────────────────────────────
    path("admin/roles", RoleListView.as_view(), name="admin-roles"),
    path("admin/approvals", PendingApprovalListView.as_view(), name="admin-approvals"),
    path("admin/approvals/<int:user_id>", ApprovalActionView.as_view(), name="admin-approval-action"),

    path("admin/users", UserViewSet.as_view({"get": "list", "post": "create"}), name="admin-users-list"),
    path(
        "admin/users/<int:pk>",
        UserViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}),
        name="admin-users-detail",
    ),

    path(
        "admin/student-profiles",
        StudentProfileViewSet.as_view({"get": "list"}),
        name="admin-student-profiles-list",
    ),
    path(
        "admin/student-profiles/<int:pk>",
        StudentProfileViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update"}),
        name="admin-student-profiles-detail",
    ),

    path(
        "admin/teacher-profiles",
        TeacherProfileViewSet.as_view({"get": "list"}),
        name="admin-teacher-profiles-list",
    ),
    path(
        "admin/teacher-profiles/<int:pk>",
        TeacherProfileViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update"}),
        name="admin-teacher-profiles-detail",
    ),
]