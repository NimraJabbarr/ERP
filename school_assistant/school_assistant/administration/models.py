"""
ADMINISTRATION APP
==================
Complaints, physical inventory, school events (with participation
tracking), and AI-generated certificates.

Cross-app references used in this file:
- Complaint.reporter / against_user, SchoolEvent.created_by_admin,
  Certificate.generated_by_admin -> accounts.User
- EventParticipation.student, Certificate.student -> accounts.StudentProfile
"""

from django.db import models


class Complaint(models.Model):
    STATUS_CHOICES = (("Open", "Open"), ("In Progress", "In Progress"), ("Resolved", "Resolved"))

    reporter = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="complaints_filed")
    complaint_type = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="Open", db_index=True)
    against_user = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="complaints_against"
    )
    attachment_url = models.URLField(blank=True, null=True)
    admin_remarks = models.TextField(blank=True, null=True)
    remarks_updated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)


class Inventory(models.Model):
    item_name = models.CharField(max_length=150)
    total_quantity = models.PositiveIntegerField()
    assigned_to_room = models.CharField(max_length=100, blank=True, db_index=True)  # Page 10 filters by room
    last_updated = models.DateTimeField(auto_now=True)


class SchoolEvent(models.Model):
    event_name = models.CharField(max_length=200)
    event_date = models.DateTimeField(db_index=True)
    venue = models.CharField(max_length=200, blank=True)
    created_by_admin = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, related_name="events_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class EventParticipation(models.Model):
    """Tracks which students took part in a school event, and at what result."""

    event = models.ForeignKey(SchoolEvent, on_delete=models.CASCADE, related_name="participants")
    student = models.ForeignKey(
        "accounts.StudentProfile", on_delete=models.CASCADE, related_name="event_participations"
    )
    role = models.CharField(max_length=50, blank=True)       # e.g. Participant / Winner / Organizer
    position = models.CharField(max_length=50, blank=True)   # e.g. "1st Place"
    certificate = models.ForeignKey(
        "Certificate", on_delete=models.SET_NULL, null=True, blank=True, related_name="event_participation"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "student")


class Certificate(models.Model):
    """AI-drafted certificates/letters, generated via the Certificates Bot."""

    CERT_TYPE_CHOICES = (
        ("leaving", "Leaving Certificate"),
        ("merit", "Merit Certificate"),
        ("clearance", "Clearance Letter"),
        ("appreciation", "Appreciation Letter"),
        ("event", "Event Certificate"),
    )

    student = models.ForeignKey("accounts.StudentProfile", on_delete=models.CASCADE, related_name="certificates")
    cert_type = models.CharField(max_length=20, choices=CERT_TYPE_CHOICES)
    generated_text = models.TextField()  # AI-drafted content, stored so it's reproducible/auditable
    generated_by_admin = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, related_name="certificates_generated"
    )
    created_at = models.DateTimeField(auto_now_add=True)
