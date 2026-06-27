from rest_framework import serializers
from administration.models import Complaint, EventParticipation, Certificate

class ParentComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ["id", "complaint_type", "description", "status", "created_at"]
        read_only_fields = ["status", "created_at"]


class ParentEventParticipationSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source="event.event_name", read_only=True)
    event_date = serializers.DateTimeField(source="event.event_date", read_only=True)
    student_name = serializers.CharField(source="student.user.full_name", read_only=True)

    class Meta:
        model = EventParticipation
        fields = [
            "id",
            "event_name",
            "event_date",
            "student_name",
            "role",
            "position",
            "certificate",
        ]
        read_only_fields = ["event_name", "event_date", "certificate", "student_name"]



class ParentCertificateSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.full_name", read_only=True)

    class Meta:
        model = Certificate
        fields = ["id", "student_name", "cert_type", "created_at"]
        read_only_fields = ["student_name", "created_at"]
