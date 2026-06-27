from rest_framework import viewsets
from accounts.models import ParentProfile, ParentStudentLink
from accounts.serializers import ParentSerializer, ParentStudentLinkSerializer
from accounts.permissions import IsParent


class ParentViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for Parent profiles."""

    serializer_class = ParentSerializer
    permission_classes = [IsParent]

    def get_queryset(self):
        # restrict to the logged-in parent only
        return ParentProfile.objects.filter(user=self.request.user)


class ParentStudentLinkViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for Parent ↔ Student relationships."""

    serializer_class = ParentStudentLinkSerializer
    permission_classes = [IsParent]

    def get_queryset(self):
        # restrict to links that belong to the logged-in parent
        return ParentStudentLink.objects.filter(parent__user=self.request.user)

    def perform_create(self, serializer):
        # Force parent to the currently logged-in parent.
        parent_profile = self.request.user.parent_profile
        serializer.save(parent=parent_profile)


