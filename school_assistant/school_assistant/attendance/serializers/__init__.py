# attendance/serializers/__init__.py

from .admin import AttendanceRecordSerializer, BehaviorLogSerializer
from .student import StudentAttendanceSerializer, StudentBehaviorLogSerializer
from .teacher import TeacherAttendanceSerializer, TeacherBehaviorLogSerializer
from .parent import ParentAttendanceSerializer, ParentBehaviorLogSerializer
