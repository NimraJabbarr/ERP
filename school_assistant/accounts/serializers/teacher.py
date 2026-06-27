from rest_framework import serializers
from accounts.models import TeacherProfile

class TeacherSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.full_name", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    cnic = serializers.CharField(read_only=True)

    class Meta:
        model = TeacherProfile
        fields = [
            "id",
            "full_name",
            "email",
            "cnic",
            "qualification",
            "specialization",
            "joining_date",
        ]

