from django.contrib import admin
from .models import (
    ClassSection,
    Subject,
    Room,
    Timetable,
    Grade,
    Assignment,
    AssignmentSubmission,
)

admin.site.register(ClassSection)
admin.site.register(Subject)
admin.site.register(Room)
admin.site.register(Timetable)
admin.site.register(Grade)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)