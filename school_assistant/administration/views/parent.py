from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsParent
from administration.models import Complaint, EventParticipation, Certificate
from administration.serializers.parent import (
    ParentComplaintSerializer, ParentEventParticipationSerializer, ParentCertificateSerializer
)

class ParentComplaintViewSet(viewsets.ModelViewSet):
    """Parents can file complaints and view their own complaints."""
    serializer_class = ParentComplaintSerializer
    permission_classes = [IsAuthenticated, IsParent]

    def get_queryset(self):
        return Complaint.objects.filter(reporter=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)


class ParentEventParticipationViewSet(viewsets.ReadOnlyModelViewSet):
    """Parents can view their child's event participations."""
    serializer_class = ParentEventParticipationSerializer
    permission_classes = [IsAuthenticated, IsParent]

    def get_queryset(self):
        return EventParticipation.objects.filter(student__parents__user=self.request.user)


class ParentCertificateViewSet(viewsets.ReadOnlyModelViewSet):
    """Parents can view their child's certificates."""
    serializer_class = ParentCertificateSerializer
    permission_classes = [IsAuthenticated, IsParent]

    def get_queryset(self):
        return Certificate.objects.filter(student__parents__user=self.request.user).order_by("-created_at")