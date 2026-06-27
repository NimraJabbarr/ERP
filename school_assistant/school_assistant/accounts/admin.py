"""
Accounts Admin Configuration
============================
Admin panel configuration for:
- Roles
- Role Permissions
- Users
- Student Profiles
- Teacher Profiles
- Parent Profiles
- Parent Student Links
"""

from django.contrib import admin
from .models import (
    Role,
    RolePermission,
    User,
    StudentProfile,
    TeacherProfile,
    ParentProfile,
    ParentStudentLink,
)
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Manage system roles.
    """

    list_display = (
        "id",
        "role_name",
        "description",
    )

    search_fields = (
        "role_name",
        "description",
    )

    ordering = ("role_name",)


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    """
    Manage role-based module permissions.
    """

    list_display = (
        "role",
        "module_name",
        "can_view",
        "can_create",
        "can_update",
        "can_delete",
    )

    list_filter = (
        "role",
        "module_name",
    )

    search_fields = (
        "role__role_name",
        "module_name",
    )

    ordering = (
        "role",
        "module_name",
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Manage system users.
    """

    list_display = (
        "id",
        "full_name",
        "email",
        "role",
        "status",
        "is_active",
        "is_staff",
        "created_at",
    )

    list_filter = (
        "role",
        "status",
        "is_active",
        "is_staff",
    )

    search_fields = (
        "full_name",
        "email",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    """
    Manage student profiles.
    """

    list_display = (
        "id",
        "user",
        "roll_number",
        "class_section",
        "scholarship_percentage",
    )

    list_filter = (
        "class_section",
        "scholarship_percentage",
    )

    search_fields = (
        "user__full_name",
        "roll_number",
        "guardian_name",
    )

    ordering = (
        "roll_number",
    )


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    """
    Manage teacher profiles.
    """

    list_display = (
        "id",
        "user",
        "cnic",
        "qualification",
        "specialization",
        "joining_date",
    )

    search_fields = (
        "user__full_name",
        "cnic",
        "specialization",
    )

    ordering = (
        "user__full_name",
    )


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    """
    Manage parent profiles.
    """

    list_display = (
        "id",
        "user",
    )

    search_fields = (
        "user__full_name",
        "user__email",
    )

    ordering = (
        "user__full_name",
    )


@admin.register(ParentStudentLink)
class ParentStudentLinkAdmin(admin.ModelAdmin):
    """
    Manage parent-child relationships.
    """

    list_display = (
        "id",
        "parent",
        "student",
        "relation",
        "is_primary_contact",
        "created_at",
    )

    list_filter = (
        "relation",
        "is_primary_contact",
    )

    search_fields = (
        "parent__user__full_name",
        "student__user__full_name",
        "student__roll_number",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )