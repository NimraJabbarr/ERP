"""
ACADEMICS APP
=============
Classes, sections, subjects, rooms, the weekly timetable, grades, and
assignments.

Cross-app references used in this file:
- Subject.assigned_teacher, Timetable.teacher, Grade.teacher,
  Assignment.teacher -> accounts.TeacherProfile
- Grade.student, AssignmentSubmission.student -> accounts.StudentProfile
"""

from django.db import models


class ClassSection(models.Model):
    """A single class + section combination, e.g. '10-A'."""

    class_name = models.CharField(max_length=20)
    section = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("class_name", "section")

    def __str__(self):
        return f"{self.class_name}-{self.section}"


class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    class_section = models.ForeignKey(ClassSection, on_delete=models.CASCADE, related_name="subjects")
    assigned_teacher = models.ForeignKey(
        "accounts.TeacherProfile", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="subjects_taught",
    )

    class Meta:
        # The same subject name can repeat across different sections,
        # each taught by a different teacher -- hence one row per section.
        unique_together = ("subject_name", "class_section")

    def __str__(self):
        return f"{self.subject_name} ({self.class_section})"


class Room(models.Model):
    """A physical classroom/room, used for timetable scheduling."""

    name = models.CharField(max_length=50)  # e.g. "Room A101"
    location = models.CharField(max_length=150, blank=True)
    capacity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Timetable(models.Model):
    """A single recurring weekly schedule slot for one class-section."""

    DAY_CHOICES = (
        ("Mon", "Monday"), ("Tue", "Tuesday"), ("Wed", "Wednesday"),
        ("Thu", "Thursday"), ("Fri", "Friday"), ("Sat", "Saturday"),
    )

    class_section = models.ForeignKey(ClassSection, on_delete=models.CASCADE, related_name="timetable_slots")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="timetable_slots")
    teacher = models.ForeignKey(
        "accounts.TeacherProfile", on_delete=models.CASCADE, related_name="timetable_slots"
    )
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name="timetable_slots")
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        # Database-level guarantees against double-booking the same
        # class, teacher, or room at the same day and time.
        unique_together = [
            ("class_section", "day", "start_time"),
            ("teacher", "day", "start_time"),
            ("room", "day", "start_time"),
        ]


class Grade(models.Model):
    EXAM_TYPE_CHOICES = (
        ("Quiz", "Quiz"), ("Mid-Term", "Mid-Term"), ("Final", "Final"), ("Assignment", "Assignment"),
    )

    student = models.ForeignKey("accounts.StudentProfile", on_delete=models.CASCADE, related_name="grades")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="grades")
    exam_type = models.CharField(max_length=30, choices=EXAM_TYPE_CHOICES)
    obtained_marks = models.DecimalField(max_digits=6, decimal_places=2)
    total_marks = models.DecimalField(max_digits=6, decimal_places=2)
    teacher = models.ForeignKey(
        "accounts.TeacherProfile", on_delete=models.SET_NULL, null=True, related_name="grades_given"
    )
    exam_date = models.DateField()

    class Meta:
        # One mark entry per student, per subject, per exam type.
        unique_together = ("student", "subject", "exam_type")


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="assignments")
    class_section = models.ForeignKey(ClassSection, on_delete=models.CASCADE, related_name="assignments")
    teacher = models.ForeignKey(
        "accounts.TeacherProfile", on_delete=models.CASCADE, related_name="assignments_posted"
    )
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(db_index=True)
    attachment_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey("accounts.StudentProfile", on_delete=models.CASCADE, related_name="submissions")
    file_url = models.URLField()

    # auto_now (not auto_now_add) because students are allowed to replace
    # their uploaded file at any time before the assignment deadline --
    # this timestamp should refresh on every resubmission.
    submitted_at = models.DateTimeField(auto_now=True)
    marks = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True, null=True)

    class Meta:
        # One submission row per student per assignment -- updated in
        # place on resubmission rather than creating duplicate rows.
        unique_together = ("assignment", "student")
