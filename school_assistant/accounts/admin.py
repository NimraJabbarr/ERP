from django.contrib import admin
from .models import Role, User, StudentProfile, TeacherProfile, ParentProfile

# In tables ko admin panel pe dekhne ke liye register kar rahe hain
admin.site.register(Role)
admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(ParentProfile)