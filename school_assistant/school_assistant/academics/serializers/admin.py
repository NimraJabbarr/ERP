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

    def validate(self, data):
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