from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsStudent
from administration.models import Complaint, EventParticipation, Certificate
from administration.serializers.student import (
    StudentComplaintSerializer, StudentEventParticipationSerializer, StudentCertificateSerializer
)

class StudentComplaintViewSet(viewsets.ModelViewSet):
    """Students can file complaints and view their own complaints."""
    serializer_class = StudentComplaintSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Complaint.objects.filter(reporter=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)


class StudentEventParticipationViewSet(viewsets.ReadOnlyModelViewSet):
    """Students can view their event participations."""
    serializer_class = StudentEventParticipationSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        return EventParticipation.objects.filter(student__user=self.request.user)


class StudentCertificateViewSet(viewsets.ReadOnlyModelViewSet):
    """Students can view their certificates."""
    serializer_class = StudentCertificateSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Certificate.objects.filter(student__user=self.request.user).order_by("-created_at")
