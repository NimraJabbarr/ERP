"""
ATTENDANCE APP
==============
Daily attendance records and student behavior/disciplinary logs.

Cross-app references used in this file:
- Attendance.student, BehaviorLog.student -> accounts.StudentProfile
- Attendance.class_section -> academics.ClassSection
- Attendance.marked_by, BehaviorLog.reported_by -> accounts.TeacherProfile
"""

from django.db import models


class Attendance(models.Model):
    STATUS_CHOICES = (("Present", "Present"), ("Absent", "Absent"), ("Leave", "Leave"))

    student = models.ForeignKey(
        "accounts.StudentProfile", on_delete=models.CASCADE, related_name="attendance_records"
    )
    class_section = models.ForeignKey(
        "academics.ClassSection", on_delete=models.CASCADE, related_name="attendance_records"
    )
    date = models.DateField(db_index=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    marked_by = models.ForeignKey(
        "accounts.TeacherProfile", on_delete=models.SET_NULL, null=True, related_name="attendance_marked"
    )

    # Supports the "lock the final daily log" requirement (Page 15) --
    # once True, the API layer should reject further edits for that day.
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "date")  # one attendance row per student per day
        indexes = [models.Index(fields=["class_section", "date"])]


class BehaviorLog(models.Model):
    """Disciplinary or notable-conduct record for a student."""

    SEVERITY_CHOICES = (("Low", "Low"), ("Medium", "Medium"), ("High", "High"))

    student = models.ForeignKey(
        "accounts.StudentProfile", on_delete=models.CASCADE, related_name="behavior_logs"
    )
    reported_by = models.ForeignKey(
        "accounts.TeacherProfile", on_delete=models.SET_NULL, null=True, related_name="behavior_logs_filed"
    )
    date = models.DateField(db_index=True)
    description = models.TextField()  # e.g. "Fighting", "Cheating", "Excellent performance in science fair"
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    action_taken = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
