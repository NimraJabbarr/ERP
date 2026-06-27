from rest_framework import viewsets
from accounts.models import StudentProfile
from accounts.serializers import StudentSerializer
from accounts.permissions import IsStudent


class StudentViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for Student profiles."""

    serializer_class = StudentSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        # restrict to the logged-in student only
        return StudentProfile.objects.filter(user=self.request.user)

