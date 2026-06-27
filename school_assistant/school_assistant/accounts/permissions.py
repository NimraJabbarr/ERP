"""
SHARED PERMISSION CLASSES
==========================
Used by views in EVERY app. Treat this file as frozen once written --
both developers import from it; if either of you needs a new permission
class, tell the other before editing this file (same rule as models.py).

Two layers are provided here:

1. Simple role checks (IsAdmin, IsTeacher, IsStudent, IsParent) -- fast,
   no extra database query beyond the already-loaded request.user.role.
   Use these for most views.

2. HasModulePermission -- a database-driven check against the
   RolePermission table, for the cases where you actually need
   finer-grained control than "is this role allowed at all" (e.g. a
   future role that can view Fees but not edit them, without a code
   change). Use this only on views where that flexibility matters --
   for everything else, the simple role checks above are enough and
   avoid an unnecessary database hit.
"""

from rest_framework.permissions import BasePermission

from accounts.models import RolePermission


class IsAdmin(BasePermission):
    """Allows access only to users with the Admin role."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role.role_name == "Admin"
        )


def is_admin_user(request) -> bool:
    """Centralized helper for Admin override."""
    return bool(
        request.user
        and request.user.is_authenticated
        and getattr(getattr(request.user, "role", None), "role_name", None) == "Admin"
    )


class IsAdminOrTeacher(BasePermission):
    def has_permission(self, request, view):
        return is_admin_user(request) or IsTeacher().has_permission(request, view)


class IsAdminOrStudent(BasePermission):
    def has_permission(self, request, view):
        return is_admin_user(request) or IsStudent().has_permission(request, view)



class IsAdminOrParent(BasePermission):
    def has_permission(self, request, view):
        return is_admin_user(request) or IsParent().has_permission(request, view)


class HasModulePermissionAllowAdmin(BasePermission):
    """Admin bypasses RolePermission checks; everyone else follows module matrix."""

    def has_permission(self, request, view):
        if is_admin_user(request):
            return True
        # Late reference to avoid NameError since HasModulePermission is declared later.
        return HasModulePermission().has_permission(request, view)



class IsTeacher(BasePermission):
    """Allows access only to users with the Teacher role."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role.role_name == "Teacher"
        )


class IsStudent(BasePermission):
    """Allows access only to users with the Student role."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role.role_name == "Student"
        )


class IsParent(BasePermission):
    """Allows access only to users with the Parent role."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role.role_name == "Parent"
        )


class HasModulePermission(BasePermission):
    """
    Checks the RolePermission table instead of a hardcoded role name.

    Usage on a view:
        class ExpenseViewSet(viewsets.ModelViewSet):
            permission_classes = [HasModulePermission]
            module_name = "Finance"   # must match a RolePermission.module_name value

    The HTTP method is mapped to which boolean column on RolePermission
    must be True for the request to be allowed.
    """

    ACTION_MAP = {
        "GET": "can_view",
        "HEAD": "can_view",
        "OPTIONS": "can_view",
        "POST": "can_create",
        "PUT": "can_update",
        "PATCH": "can_update",
        "DELETE": "can_delete",
    }

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        module_name = getattr(view, "module_name", None)
        action_field = self.ACTION_MAP.get(request.method)
        if not module_name or not action_field:
            return False

        try:
            permission_row = RolePermission.objects.get(
                role=request.user.role, module_name=module_name
            )
        except RolePermission.DoesNotExist:
            return False

        return getattr(permission_row, action_field, False)