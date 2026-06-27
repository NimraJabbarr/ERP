from rest_framework import serializers
from accounts.models import StudentProfile

class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.full_name", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    # Admin-only fields (security): keep them immutable for Student role.
    roll_number = serializers.CharField(read_only=True)
    class_section_id = serializers.IntegerField(read_only=True)
    scholarship_percentage = serializers.IntegerField(read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            "id",
            "full_name",
            "email",
            "roll_number",
            "class_section_id",
            "guardian_name",
            "guardian_phone",
            "scholarship_percentage",
            "date_of_birth",
        ]

