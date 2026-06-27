from rest_framework import serializers
from attendance.models import Attendance, BehaviorLog

class ParentAttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.full_name", read_only=True)

    class Meta:
        model = Attendance
        fields = ["id", "student_name", "date", "status", "class_section", "is_locked"]
        read_only_fields = ["student_name", "is_locked"]


class ParentBehaviorLogSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.full_name", read_only=True)
    reported_by_name = serializers.CharField(source="reported_by.user.full_name", read_only=True)

    class Meta:
        model = BehaviorLog
        fields = ["id", "student_name", "date", "description", "severity", "action_taken", "reported_by_name"]
        read_only_fields = ["student_name", "reported_by_name"]
