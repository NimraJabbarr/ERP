"""
Combines this app's role-split url files into one importable urls module.
Written once at setup -- the actual route additions happen inside
admin.py / teacher.py / student.py / parent.py, not here.
"""

from django.urls import path, include

urlpatterns = [
    path("", include("accounts.urls.admin")),
    path("", include("accounts.urls.student")),
    path("", include("accounts.urls.teacher")),
    path("", include("accounts.urls.parent")),
    # NOTE: accounts/urls/teacher.py, student.py, parent.py stay empty --
    # auth (register/login/profile/password) is shared and already wired
    # above. Dev B only needs to add routes here if a role ever needs an
    # accounts-specific endpoint that ISN'T shared auth.
]