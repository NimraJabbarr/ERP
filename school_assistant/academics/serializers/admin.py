"""
ACADEMICS -- ADMIN-ROLE SERIALIZERS
=====================================
Covers: Classes & Subjects Builder (Page 8) and the Timetable & Rooms
Builder. Grades/Assignments are NOT here -- those are entered by
Teachers, so they belong in academics/serializers/teacher.py (Dev B).
"""

from rest_framework import serializers

from academics.models import ClassSection, Subject, Room, Timetable


class ClassSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSection
        fields = ["id", "class_name", "section", "created_at"]

    #  NEW VALIDATION: Sirf PG se 10 tak ki classes allow hain
    def validate_class_name(self, value):
        ALLOWED_CLASSES = [
            'PG', 'Nursery', 'KG',
            '1', '2', '3', '4', '5',
            '6', '7', '8', '9', '10'
        ]
        if value not in ALLOWED_CLASSES:
            raise serializers.ValidationError(
                f"Invalid class name. Allowed: {', '.join(ALLOWED_CLASSES)}"
            )
        return value

    # NEW VALIDATION: Section single alphabet hona chahiye
    def validate_section(self, value):
        if not value.isalpha() or len(value) != 1:
            raise serializers.ValidationError("Section must be a single letter (A-Z).")
        return value.upper()


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "subject_name", "class_section", "assigned_teacher"]


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "name", "location", "capacity"]


class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = ["id", "class_section", "subject", "teacher", "room", "day", "start_time", "end_time"]

    # NEW VALIDATION: Sirf Monday-Saturday allow hain
    def validate_day(self, value):
        ALLOWED_DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        if value not in ALLOWED_DAYS:
            raise serializers.ValidationError(f"Invalid day. Allowed: {', '.join(ALLOWED_DAYS)}")
        return value

    def validate(self, data):
        #  NEW VALIDATION: Start time end time se pehle hona chahiye
        if data.get('start_time') and data.get('end_time'):
            if data['start_time'] >= data['end_time']:
                raise serializers.ValidationError("Start time must be before end time.")

        # Model-level unique_together already blocks DB-level clashes;
        # this gives the same check a friendlier error message at the API layer.
        qs = Timetable.objects.filter(day=data["day"], start_time=data["start_time"])
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.filter(class_section=data["class_section"]).exists():
            raise serializers.ValidationError("This class already has a slot at that day/time.")
        if qs.filter(teacher=data["teacher"]).exists():
            raise serializers.ValidationError("This teacher is already booked at that day/time.")
        if data.get("room") and qs.filter(room=data["room"]).exists():
            raise serializers.ValidationError("This room is already booked at that day/time.")
        return data