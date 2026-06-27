# administration/serializers/__init__.py

from .admin import (
    ComplaintSerializer,
    InventorySerializer,
    SchoolEventSerializer,
    EventParticipationSerializer,
    CertificateSerializer,
    CertificateGenerateSerializer,
)

from .student import (
    StudentComplaintSerializer,
    StudentEventParticipationSerializer,
    StudentCertificateSerializer,
)

from .teacher import (
    TeacherComplaintSerializer,
    TeacherEventSerializer,
    TeacherEventParticipationSerializer,
)

from .parent import (
    ParentComplaintSerializer,
    ParentEventParticipationSerializer,
    ParentCertificateSerializer,
)
