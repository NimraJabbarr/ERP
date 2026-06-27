"""
ACCOUNTS APP
============
Handles authentication, roles, and role-specific profile data for all
four user types in the system: Admin, Teacher, Student, and Parent.

Cross-app references used in this file:
- StudentProfile.class_section -> academics.ClassSection
(Other apps reference accounts.User / accounts.StudentProfile /
accounts.TeacherProfile back -- see their own models.py files.)
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError

class Role(models.Model):
    """
    Simple lookup table so that User.role is a clean foreign key instead
    of a hardcoded enum.

    UPDATE: originally this was NOT paired with a permissions table, since
    the 4 roles were fixed by the spec. The project now needs to support
    adding new roles / adjusting access rules without a code deployment,
    so RolePermission below provides that flexibility.
    """
    role_name = models.CharField(max_length=20, unique=True)  # Admin / Teacher / Student / Parent
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.role_name


class RolePermission(models.Model):
    """
    Per-role, per-module access control, stored in the database instead
    of hardcoded in code. This is what makes the system flexible for the
    future: adding a brand-new role (e.g. "Accountant") or changing what
    an existing role can access just means inserting/editing rows here --
    no code change or redeployment needed.

    `module_name` is a free-text label matching a feature area (e.g.
    "Attendance", "Fees", "Inventory", "Chatbot") rather than a foreign
    key to a table, since modules are a logical grouping of several
    models/views, not a single database table.

    How this gets used in views (once built): a permission_classes check
    looks up RolePermission.objects.get(role=request.user.role,
    module_name="Fees") and inspects can_view/can_create/etc., instead of
    a hardcoded `if request.user.role.role_name == "Admin"` check.
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="permissions")
    module_name = models.CharField(max_length=50)  # e.g. "Attendance", "Fees", "Inventory", "Chatbot"
    can_view = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    class Meta:
        unique_together = ("role", "module_name")  # one permission row per role per module

    def __str__(self):
        return f"{self.role.role_name} - {self.module_name}"


class UserManager(BaseUserManager):
    """
    Custom manager required because this project logs in with email
    instead of Django's default username field.
    """

    def create_user(self, email, full_name, role, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, role, password=None, **extra_fields):
        # NOTE: the `role` Role row must already exist in the database
        # before this is called -- see the seeding step in README_SETUP.md.
        extra_fields.setdefault("status", "Active")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, full_name, role, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Central identity table for every role in the system. Role-specific
    extra fields live in the *Profile models below (one-to-one) -- this
    keeps the User table lean and avoids nullable columns that only
    apply to a single role.
    """
    STATUS_CHOICES = (
        ("Pending", "Pending"),    # awaiting Admin approval (applies to Teacher/Student/Parent signups)
        ("Active", "Active"),
        ("Rejected", "Rejected"),
    )

    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="users")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Required by Django's auth framework.
    is_active = models.BooleanField(default=True)   # account enabled/disabled -- separate from `status` above
    is_staff = models.BooleanField(default=False)    # grants access to the Django admin site only

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "role"]

    objects = UserManager()
    def save(self, *args, **kwargs):
        """
        Enforces "Admin is a single pre-set account, no signup" (spec).
        """
        if self.role_id and self.role.role_name == "Admin":
            already_exists = User.objects.filter(role__role_name="Admin").exclude(pk=self.pk).exists()
            if already_exists:
                raise ValidationError("Only one Admin account is allowed in this system.")
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.full_name} ({self.role.role_name})"


class StudentProfile(models.Model):
    """Extra fields specific to Student accounts."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")

    # Nullable on purpose: a student only picks their CLASS at signup
    # (Page 3 of the spec). The roll number is assigned by the Admin
    # later, during account approval (Page 7) -- it is not entered by the
    # student. A parent registering needs this roll number to already
    # exist, so the workflow order is always: student approved + roll
    # number assigned FIRST, then the parent can register and link to
    # them via ParentStudentLink below.
    roll_number = models.CharField(max_length=20, unique=True, null=True, blank=True, db_index=True)

    class_section = models.ForeignKey("academics.ClassSection", on_delete=models.PROTECT, related_name="students")

    # Display-only fields -- NOT used for access control. ParentStudentLink
    # below is the actual source of truth for who can log in as this
    # child's parent.
    guardian_name = models.CharField(max_length=150, blank=True)
    guardian_phone = models.CharField(max_length=20, blank=True)

    scholarship_percentage = models.PositiveSmallIntegerField(
        choices=[(0, "0%"), (50, "50%"), (100, "100%")], default=0
    )
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.roll_number or 'unassigned'} - {self.user.full_name}"


class TeacherProfile(models.Model):
    """Extra fields specific to Teacher accounts."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher_profile")
    cnic = models.CharField(max_length=20, unique=True)
    qualification = models.CharField(max_length=150, blank=True)
    specialization = models.CharField(max_length=150, blank=True)
    joining_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.full_name


class ParentProfile(models.Model):
    """Extra fields specific to Parent accounts."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="parent_profile")

    # The actual parent <-> child relationship lives in ParentStudentLink
    # below (a many-to-many bridge table), NOT as a direct foreign key here.
    children = models.ManyToManyField(StudentProfile, through="ParentStudentLink", related_name="parents")

    def __str__(self):
        return self.user.full_name


class ParentStudentLink(models.Model):
    """
    *** Fixes the original schema's parent-child design flaw. ***

    The original design gave Parent_Profile a single `child_student_id`
    foreign key. That broke in two real scenarios:
      1. A parent with more than one child enrolled would need a SEPARATE
         Parent user account per child (since ParentProfile was
         one-to-one with User).
      2. A single child could never have two independent parent logins
         at the same time (e.g. both Father and Mother).

    This bridge table fixes both problems:
      - One parent login can be linked to MANY StudentProfile rows.
      - One student can be linked to MANY ParentProfile rows.
    """
    RELATION_CHOICES = (
        ("Father", "Father"),
        ("Mother", "Mother"),
        ("Guardian", "Guardian"),
    )

    parent = models.ForeignKey(ParentProfile, on_delete=models.CASCADE, related_name="child_links")
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="parent_links")
    relation = models.CharField(max_length=10, choices=RELATION_CHOICES)

    # When both a Father and Mother account are linked to the same child,
    # this flags which one should get priority for WhatsApp/email alerts.
    is_primary_contact = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("parent", "student")  # prevents duplicate link rows
        indexes = [models.Index(fields=["student", "parent"])]

    def __str__(self):
        return f"{self.parent} -> {self.student} ({self.relation})"