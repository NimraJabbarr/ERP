"""
ADMINISTRATION -- ADMIN-ROLE SERIALIZERS
===========================================
"""

from rest_framework import serializers

from administration.models import Complaint, Inventory, SchoolEvent, EventParticipation, Certificate


class ComplaintSerializer(serializers.ModelSerializer):
    reporter_name = serializers.CharField(source="reporter.full_name", read_only=True)
    reporter_role = serializers.CharField(source="reporter.role.role_name", read_only=True)

    class Meta:
        model = Complaint
        fields = [
            "id", "reporter", "reporter_name", "reporter_role", "complaint_type",
            "description", "status", "against_user", "attachment_url",
            "admin_remarks", "remarks_updated_at", "created_at", "resolved_at",
        ]
        read_only_fields = ["reporter", "created_at"]

    # VALIDATION: Complaint type capitalize ho
    def validate_complaint_type(self, value):
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Complaint type must be at least 2 characters long.")
        return value.strip().title()

    # VALIDATION: Description minimum 10 characters
    def validate_description(self, value):
        if not value or len(value.strip()) < 10:
            raise serializers.ValidationError("Description must be at least 10 characters long.")
        return value.strip()


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ["id", "item_name", "total_quantity", "assigned_to_room", "last_updated"]

    # VALIDATION: Quantity negative na ho
    def validate_total_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return value


class SchoolEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolEvent
        fields = ["id", "event_name", "event_date", "venue", "created_by_admin", "created_at"]
        read_only_fields = ["created_by_admin", "created_at"]

    #  VALIDATION: Event name capitalize ho
    def validate_event_name(self, value):
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError("Event name must be at least 3 characters long.")
        return value.strip().title()


class EventParticipationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.full_name", read_only=True)

    class Meta:
        model = EventParticipation
        fields = ["id", "event", "student", "student_name", "role", "position", "certificate", "created_at"]

    #  VALIDATION: Position sirf predefined values allow karein
    def validate_position(self, value):
        ALLOWED_POSITIONS = ['1st Place', '2nd Place', '3rd Place', 'Winner', 'Participant', 'Organizer']
        if value and value not in ALLOWED_POSITIONS:
            raise serializers.ValidationError(
                f"Invalid position. Allowed: {', '.join(ALLOWED_POSITIONS)}"
            )
        return value


class CertificateSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.full_name", read_only=True)

    class Meta:
        model = Certificate
        fields = [
            "id", "student", "student_name", "cert_type",
            "generated_text", "generated_by_admin", "created_at",
        ]
        read_only_fields = ["generated_by_admin", "created_at"]


class CertificateGenerateSerializer(serializers.Serializer):
    """POST /api/admin/certificates/generate -- input-only serializer for the generation action."""

    student_id = serializers.IntegerField()
    cert_type = serializers.ChoiceField(choices=["leaving", "merit", "clearance", "appreciation", "event"])
    custom_note = serializers.CharField(required=False, allow_blank=True)