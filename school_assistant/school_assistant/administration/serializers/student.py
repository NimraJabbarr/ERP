from rest_framework import serializers
from administration.models import Complaint, EventParticipation, Certificate

class StudentComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ["id", "complaint_type", "description", "status", "attachment_url", "created_at"]
        read_only_fields = ["status", "created_at"]


class StudentEventParticipationSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source="event.event_name", read_only=True)
    event_date = serializers.DateTimeField(source="event.event_date", read_only=True)

    class Meta:
        model = EventParticipation
        fields = ["id", "event", "event_name", "event_date", "role", "position", "certificate", "created_at"]
        read_only_fields = ["event_name", "event_date", "certificate", "created_at"]


class StudentCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "cert_type", "generated_text", "created_at"]
        read_only_fields = ["generated_text", "created_at"]
