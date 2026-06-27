"""
ACCOUNTS -- ADMIN-ROLE SERIALIZERS
===================================
Covers: User management, account approvals, role listing, and the
shared authentication serializers.
"""

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import User, Role, StudentProfile, TeacherProfile, ParentProfile, ParentStudentLink

# ── SHARED AUTH SERIALIZERS (used by every role) ────────────────────────

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    role_name = serializers.ChoiceField(choices=["Teacher", "Student", "Parent"], write_only=True)

    class_section_id = serializers.IntegerField(write_only=True, required=False)
    cnic = serializers.CharField(write_only=True, required=False)
    child_roll_number = serializers.CharField(write_only=True, required=False)
    relation = serializers.ChoiceField(choices=["Father", "Mother", "Guardian"], write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "id", "full_name", "email", "password", "role_name",
            "class_section_id", "cnic", "child_roll_number", "relation",
        ]

    def validate(self, data):
        role_name = data["role_name"]
        if role_name == "Student" and not data.get("class_section_id"):
            raise serializers.ValidationError({"class_section_id": "Required for Student signup."})
        if role_name == "Teacher" and not data.get("cnic"):
            raise serializers.ValidationError({"cnic": "Required for Teacher signup."})
        if role_name == "Parent":
            if not data.get("child_roll_number"):
                raise serializers.ValidationError({"child_roll_number": "Required for Parent signup."})
            if not data.get("relation"):
                raise serializers.ValidationError({"relation": "Required for Parent signup."})
            if not StudentProfile.objects.filter(roll_number=data["child_roll_number"]).exists():
                raise serializers.ValidationError(
                    {"child_roll_number": "No student found with this roll number. Ask Admin to confirm it first."}
                )
        return data

    def create(self, validated_data):
        role_name = validated_data.pop("role_name")
        class_section_id = validated_data.pop("class_section_id", None)
        cnic = validated_data.pop("cnic", None)
        child_roll_number = validated_data.pop("child_roll_number", None)
        relation = validated_data.pop("relation", None)
        password = validated_data.pop("password")

        role = Role.objects.get(role_name=role_name)
        user = User.objects.create_user(
            email=validated_data["email"], full_name=validated_data["full_name"],
            role=role, password=password,
        )

        if role_name == "Student":
            StudentProfile.objects.create(user=user, class_section_id=class_section_id)
        elif role_name == "Teacher":
            TeacherProfile.objects.create(user=user, cnic=cnic)
        elif role_name == "Parent":
            parent_profile = ParentProfile.objects.create(user=user)
            student = StudentProfile.objects.get(roll_number=child_roll_number)
            ParentStudentLink.objects.create(parent=parent_profile, student=student, relation=relation)

        return user


class ProfileSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source="role.role_name", read_only=True)

    class Meta:
        model = User
        fields = ["id", "full_name", "email", "role_name", "status", "created_at"]
        read_only_fields = ["email", "status", "created_at"]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])


# ── ADMIN-ONLY SERIALIZERS ───────────────────────────────────────────────

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "role_name", "description"]


class PendingUserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source="role.role_name", read_only=True)

    class Meta:
        model = User
        fields = ["id", "full_name", "email", "role_name", "status", "created_at"]


class ApprovalActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["approve", "reject"])
    roll_number = serializers.CharField(required=False, allow_blank=True)


class StudentProfileAdminSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.full_name", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            "id", "full_name", "email", "roll_number", "class_section",
            "guardian_name", "guardian_phone", "scholarship_percentage", "date_of_birth",
        ]


class TeacherProfileAdminSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.full_name", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = TeacherProfile
        fields = ["id", "full_name", "email", "cnic", "qualification", "specialization", "joining_date"]


class UserAdminSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source="role.role_name", read_only=True)

    class Meta:
        model = User
        fields = ["id", "full_name", "email", "role", "role_name", "status", "is_active", "created_at"]
        read_only_fields = ["created_at"]

    def validate_role(self, value):
        if value.role_name == "Admin":
            existing = User.objects.filter(role__role_name="Admin")
            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise serializers.ValidationError("Only one Admin account is allowed in this system.")
        return value