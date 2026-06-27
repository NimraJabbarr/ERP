"""
ATTENDANCE -- ADMIN-ROLE SERIALIZERS
=======================================
Admin doesn't MARK attendance (that's Teacher's job -- teacher.py, Dev B)
-- Admin only views aggregated summaries and the Behavior Log overview.
"""

from rest_framework import serializers

from attendance.models import Attendance, BehaviorLog


class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.full_name", read_only=True)

    class Meta:
        model = Attendance
        fields = ["id", "student", "student_name", "class_section", "date", "status", "is_locked"]


class BehaviorLogSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.full_name", read_only=True)
    reported_by_name = serializers.CharField(source="reported_by.user.full_name", read_only=True)

    class Meta:
        model = BehaviorLog
        fields = [
            "id", "student", "student_name", "reported_by", "reported_by_name",
            "date", "description", "severity", "action_taken", "created_at",
        ]