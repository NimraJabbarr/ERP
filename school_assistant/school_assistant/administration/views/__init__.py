# administration/views/__init__.py

from .admin import (
    ComplaintViewSet, InventoryViewSet, InventorySummaryView,
    SchoolEventViewSet, EventParticipationViewSet,
    CertificateViewSet, CertificateGenerateView, CertificateDownloadView,
)

from .student import (
    StudentComplaintViewSet, StudentEventParticipationViewSet, StudentCertificateViewSet,
)

from .teacher import (
    TeacherComplaintViewSet, TeacherEventViewSet, TeacherEventParticipationViewSet,
)

from .parent import (
    ParentComplaintViewSet, ParentEventParticipationViewSet, ParentCertificateViewSet,
)
