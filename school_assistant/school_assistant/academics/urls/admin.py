from django.urls import path

from academics.views.admin import ClassSectionViewSet, SubjectViewSet, RoomViewSet, TimetableViewSet

urlpatterns = [
    path("admin/classes", ClassSectionViewSet.as_view({"get": "list", "post": "create"})),
    path("admin/classes/<int:pk>", ClassSectionViewSet.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
    )),

    path("admin/subjects", SubjectViewSet.as_view({"get": "list", "post": "create"})),
    path("admin/subjects/<int:pk>", SubjectViewSet.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
    )),

    path("admin/rooms", RoomViewSet.as_view({"get": "list", "post": "create"})),
    path("admin/rooms/<int:pk>", RoomViewSet.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
    )),

    path("admin/timetable", TimetableViewSet.as_view({"get": "list", "post": "create"})),
    path("admin/timetable/<int:pk>", TimetableViewSet.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
    )),
]