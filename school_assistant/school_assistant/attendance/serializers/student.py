from rest_framework import serializers
from attendance.models import Attendance, BehaviorLog

class StudentAttendanceSerializer(serializers.ModelSerializer):
    class_section_name = serializers.CharField(source="class_section.class_name", read_only=True)

    class Meta:
        model = Attendance
        fields = ["id", "date", "status", "class_section_name", "is_locked"]
        read_only_fields = ["is_locked"]


class StudentBehaviorLogSerializer(serializers.ModelSerializer):
    reported_by_name = serializers.CharField(source="reported_by.user.full_name", read_only=True)

    class Meta:
        model = BehaviorLog
        fields = ["id", "date", "description", "severity", "action_taken", "reported_by_name"]
        read_only_fields = ["reported_by_name"]
