from rest_framework import viewsets
from accounts.models import TeacherProfile
from accounts.serializers import TeacherSerializer
from accounts.permissions import IsTeacher  # make sure you have this

class TeacherViewSet(viewsets.ModelViewSet):
    """
    CRUD endpoints for Teacher profiles.
    """
    serializer_class = TeacherSerializer
    permission_classes = [IsTeacher]

    def get_queryset(self):
        # restrict to the logged-in teacher only
        return TeacherProfile.objects.filter(user=self.request.user)
