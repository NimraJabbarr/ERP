# academics/views/__init__.py

from .admin import ClassSectionViewSet, SubjectViewSet, RoomViewSet, TimetableViewSet
from .student import StudentGradeViewSet, StudentAssignmentViewSet, StudentSubmissionViewSet
from .teacher import TeacherGradeViewSet, TeacherAssignmentViewSet, TeacherSubmissionViewSet
from .parent import ParentGradeViewSet, ParentSubmissionViewSet
