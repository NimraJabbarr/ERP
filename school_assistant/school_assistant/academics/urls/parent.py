from django.urls import path
from academics.views.parent import (
    ParentGradeViewSet, ParentSubmissionViewSet
)

urlpatterns = [
    path("parent/grades", ParentGradeViewSet.as_view({"get": "list"})),
    path("parent/grades/<int:pk>", ParentGradeViewSet.as_view({"get": "retrieve"})),

    path("parent/submissions", ParentSubmissionViewSet.as_view({"get": "list"})),
    path("parent/submissions/<int:pk>", ParentSubmissionViewSet.as_view({"get": "retrieve"})),
]
