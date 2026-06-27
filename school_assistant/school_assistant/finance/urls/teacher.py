from django.urls import path
from finance.views.teacher import TeacherExpenseViewSet

urlpatterns = [
    path("teacher/expenses", TeacherExpenseViewSet.as_view({"get": "list", "post": "create"})),
    path("teacher/expenses/<int:pk>", TeacherExpenseViewSet.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
    )),
]
