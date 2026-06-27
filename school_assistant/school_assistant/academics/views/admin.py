"""
ACADEMICS -- ADMIN-ROLE VIEWS
================================
"""

from rest_framework import viewsets

from academics.models import ClassSection, Subject, Room, Timetable
from accounts.permissions import IsAdmin
from academics.serializers.admin import (
    ClassSectionSerializer, SubjectSerializer, RoomSerializer, TimetableSerializer,
)


class ClassSectionViewSet(viewsets.ModelViewSet):
    """CRUD /api/admin/classes"""
    queryset = ClassSection.objects.all()
    serializer_class = ClassSectionSerializer
    permission_classes = [IsAdmin]


class SubjectViewSet(viewsets.ModelViewSet):
    """CRUD /api/admin/subjects"""
    queryset = Subject.objects.select_related("class_section", "assigned_teacher").all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAdmin]


class RoomViewSet(viewsets.ModelViewSet):
    """CRUD /api/admin/rooms"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdmin]


class TimetableViewSet(viewsets.ModelViewSet):
    """CRUD /api/admin/timetable"""
    queryset = Timetable.objects.select_related("class_section", "subject", "teacher", "room").all()
    serializer_class = TimetableSerializer
    permission_classes = [IsAdmin]