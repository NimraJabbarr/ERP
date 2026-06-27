from rest_framework import serializers
from attendance.models import Attendance, BehaviorLog

class TeacherAttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.full_name", read_only=True)

    class Meta:
        model = Attendance
        fields = ["id", "student", "student_name", "class_section", "date", "status", "is_locked"]
        read_only_fields = ["is_locked"]


class TeacherBehaviorLogSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.full_name", read_only=True)

    class Meta:
        model = BehaviorLog
        fields = ["id", "student", "student_name", "date", "description", "severity", "action_taken", "created_at"]
