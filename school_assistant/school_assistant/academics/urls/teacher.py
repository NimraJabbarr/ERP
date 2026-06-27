from django.urls import path
from academics.views.teacher import (
    TeacherGradeViewSet, TeacherAssignmentViewSet, TeacherSubmissionViewSet
)

urlpatterns = [
    path("teacher/grades", TeacherGradeViewSet.as_view({"get": "list", "post": "create"})),
    path("teacher/grades/<int:pk>", TeacherGradeViewSet.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
    )),

    path("teacher/assignments", TeacherAssignmentViewSet.as_view({"get": "list", "post": "create"})),
    path("teacher/assignments/<int:pk>", TeacherAssignmentViewSet.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
    )),

    path("teacher/submissions", TeacherSubmissionViewSet.as_view({"get": "list"})),
    path("teacher/submissions/<int:pk>", TeacherSubmissionViewSet.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update"}
    )),
]
