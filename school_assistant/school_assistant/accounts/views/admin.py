"""
ACCOUNTS -- ADMIN-ROLE VIEWS
==============================
Shared auth views (Register/Profile/ChangePassword -- used by every
role) plus Admin-exclusive views (approvals, user management, roles).

Login itself uses djangorestframework-simplejwt's built-in
TokenObtainPairView directly in urls/admin.py -- no custom view needed.
"""

from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User, Role, StudentProfile, TeacherProfile
from accounts.permissions import IsAdmin
from accounts.serializers.admin import (
    RegisterSerializer, ProfileSerializer, ChangePasswordSerializer,
    RoleSerializer, PendingUserSerializer, ApprovalActionSerializer,
    StudentProfileAdminSerializer, TeacherProfileAdminSerializer, UserAdminSerializer,
)

password_reset_token = PasswordResetTokenGenerator()


# ── SHARED AUTH VIEWS (every role uses these) ────────────────────────────

class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register -- open to anyone, no auth required."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    """GET/PUT /api/auth/profile -- works for whichever role is logged in."""
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """PUT /api/auth/change-password"""
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response({"detail": "Password updated successfully."})


class PasswordResetRequestView(APIView):
    """POST /api/auth/password-reset"""
    permission_classes = [AllowAny]

    def post(self, request):
        # Circular import se bachne ke liye local import kiya hai
        from accounts.serializers.admin import PasswordResetRequestSerializer
        
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(email=serializer.validated_data["email"]).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = password_reset_token.make_token(user)
            logger_message = f"Password reset requested for {user.email} -- uid={uid}, token={token}"
            print(logger_message)  # Console / Terminal mein token dikhega

        return Response({"detail": "If that email is registered, a reset link has been sent."})


class PasswordResetConfirmView(APIView):
    """POST /api/auth/password-reset/confirm"""
    permission_classes = [AllowAny]

    def post(self, request):
        # Circular import se bachne ke liye local import kiya hai
        from accounts.serializers.admin import PasswordResetConfirmSerializer
        
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            uid = force_str(urlsafe_base64_decode(data["uid"]))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": "Invalid reset link."}, status=status.HTTP_400_BAD_REQUEST)

        if not password_reset_token.check_token(user, data["token"]):
            return Response({"detail": "Invalid or expired reset link."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(data["new_password"])
        user.save()
        return Response({"detail": "Password reset successfully. You can now log in."})


# ── ADMIN-ONLY VIEWS ───────────────────────────────────────────────────────

class RoleListView(generics.ListAPIView):
    """GET /api/admin/roles"""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdmin]


class PendingApprovalListView(generics.ListAPIView):
    """GET /api/admin/approvals -- list every account awaiting approval."""
    queryset = User.objects.filter(status="Pending")
    serializer_class = PendingUserSerializer
    permission_classes = [IsAdmin]


class ApprovalActionView(APIView):
    """PUT /api/admin/approvals/{user_id}"""
    permission_classes = [IsAdmin]

    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = ApprovalActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action = serializer.validated_data["action"]

        if action == "approve":
            user.status = "Active"
            user.save()

            if user.role.role_name == "Student":
                roll_number = serializer.validated_data.get("roll_number")
                if not roll_number:
                    return Response(
                        {"roll_number": "A roll number must be assigned when approving a student."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                student_profile = StudentProfile.objects.get(user=user)
                student_profile.roll_number = roll_number
                student_profile.save()
        else:
            user.status = "Rejected"
            user.save()

        return Response({"detail": f"User {action}d successfully.", "status": user.status})


class UserViewSet(viewsets.ModelViewSet):
    """CRUD /api/admin/users"""
    queryset = User.objects.all().order_by("-created_at")
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdmin]


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.select_related("user").all()
    serializer_class = StudentProfileAdminSerializer
    permission_classes = [IsAdmin]


class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.select_related("user").all()
    serializer_class = TeacherProfileAdminSerializer
    permission_classes = [IsAdmin]