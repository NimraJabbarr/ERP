from django.urls import path
from academics.views.student import (
    StudentGradeViewSet, StudentAssignmentViewSet, StudentSubmissionViewSet
)

urlpatterns = [
    path("student/grades", StudentGradeViewSet.as_view({"get": "list"})),
    path("student/grades/<int:pk>", StudentGradeViewSet.as_view({"get": "retrieve"})),

    path("student/assignments", StudentAssignmentViewSet.as_view({"get": "list"})),
    path("student/assignments/<int:pk>", StudentAssignmentViewSet.as_view({"get": "retrieve"})),

    path("student/submissions", StudentSubmissionViewSet.as_view({"get": "list", "post": "create"})),
    path("student/submissions/<int:pk>", StudentSubmissionViewSet.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
    )),
]
