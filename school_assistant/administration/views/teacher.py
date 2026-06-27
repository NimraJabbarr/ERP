from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsTeacher
from administration.models import Complaint, SchoolEvent, EventParticipation
from administration.serializers.teacher import (
    TeacherComplaintSerializer, TeacherEventSerializer, TeacherEventParticipationSerializer
)

class TeacherComplaintViewSet(viewsets.ReadOnlyModelViewSet):
    """Teachers can view complaints filed against them or filed by them."""
    serializer_class = TeacherComplaintSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return Complaint.objects.filter(reporter=self.request.user) | Complaint.objects.filter(against_user=self.request.user)


class TeacherEventViewSet(viewsets.ReadOnlyModelViewSet):
    """Teachers can view events they are involved in.

    SchoolEvent is created/edited/deleted only by Admin (via created_by_admin).
    """
    serializer_class = TeacherEventSerializer
    permission_classes = [IsAuthenticated, IsTeacher]


    def get_queryset(self):
        # SchoolEvent has no `teacher` FK; it uses `created_by_admin`.
        return SchoolEvent.objects.filter(created_by_admin=self.request.user).order_by("-event_date")




class TeacherEventParticipationViewSet(viewsets.ReadOnlyModelViewSet):
    """Teachers can view student participations in events they manage."""
    serializer_class = TeacherEventParticipationSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return EventParticipation.objects.filter(
            event__created_by_admin=self.request.user
        ).select_related("student__user", "event")
