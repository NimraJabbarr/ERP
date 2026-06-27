from rest_framework import serializers
from administration.models import Complaint, SchoolEvent, EventParticipation

class TeacherComplaintSerializer(serializers.ModelSerializer):
    reporter_name = serializers.CharField(source="reporter.full_name", read_only=True)

    class Meta:
        model = Complaint
        fields = ["id", "reporter_name", "complaint_type", "description", "status", "created_at"]
        read_only_fields = ["reporter_name", "status", "created_at"]


class TeacherEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolEvent
        fields = ["id", "event_name", "event_date", "venue", "created_at"]
        read_only_fields = ["created_at"]


class TeacherEventParticipationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.full_name", read_only=True)

    class Meta:
        model = EventParticipation
        fields = ["id", "event", "student", "student_name", "role", "position", "created_at"]
        read_only_fields = ["student_name", "created_at"]
