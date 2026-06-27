from django.urls import path
from administration.views.teacher import (
    TeacherComplaintViewSet, TeacherEventViewSet, TeacherEventParticipationViewSet
)

urlpatterns = [
    path("teacher/complaints", TeacherComplaintViewSet.as_view({"get": "list"})),
    path("teacher/complaints/<int:pk>", TeacherComplaintViewSet.as_view({"get": "retrieve"})),

    path("teacher/events", TeacherEventViewSet.as_view({"get": "list", "post": "create"})),
    path("teacher/events/<int:pk>", TeacherEventViewSet.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
    )),

    path("teacher/events/participations", TeacherEventParticipationViewSet.as_view({"get": "list"})),
    path("teacher/events/participations/<int:pk>", TeacherEventParticipationViewSet.as_view({"get": "retrieve"})),
]
