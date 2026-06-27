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
admin.site.register(Subject)
admin.site.register(Room)
admin.site.register(Timetable)
admin.site.register(Grade)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)
from django.contrib import admin
from academics.models import ClassSection

@admin.register(ClassSection)
class ClassSectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'class_name', 'section']
    
    def save_model(self, request, obj, form, change):
        ALLOWED_CLASSES = ['PG', 'Nursery', 'KG', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        if obj.class_name not in ALLOWED_CLASSES:
            from django.core.exceptions import ValidationError
            raise ValidationError(f"Invalid class name. Allowed: {', '.join(ALLOWED_CLASSES)}")
        super().save_model(request, obj, form, change)
