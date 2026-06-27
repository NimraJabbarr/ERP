from rest_framework import serializers
from accounts.models import ParentProfile, ParentStudentLink, StudentProfile

class ParentSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.full_name", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = ParentProfile
        fields = ["id", "full_name", "email"]

class ParentStudentLinkSerializer(serializers.ModelSerializer):
    student_roll_number = serializers.CharField(source="student.roll_number", read_only=True)
    student_name = serializers.CharField(source="student.user.full_name", read_only=True)

    # Security: parent can’t be reassigned by a client.
    parent = serializers.PrimaryKeyRelatedField(read_only=True)

    # Security: prevent parent from guessing/linking arbitrary student IDs.
    roll_number = serializers.CharField(write_only=True)

    def validate_roll_number(self, value):
        try:
            return StudentProfile.objects.get(roll_number=value)
        except StudentProfile.DoesNotExist:
            raise serializers.ValidationError("No student found with this roll number.")

    def create(self, validated_data):
        # Pop roll_number -> StudentProfile instance
        student_profile = validated_data.pop("roll_number")
        validated_data["student"] = student_profile
        return super().create(validated_data)

    class Meta:
        model = ParentStudentLink
        fields = [
            "id",
            "parent",
            "student",
            "relation",
            "is_primary_contact",
            "student_roll_number",
            "student_name",
            "roll_number",
        ]
        read_only_fields = ["parent", "student"]

