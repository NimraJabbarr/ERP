from django.urls import path
from finance.views.student import StudentFeeViewSet, StudentPaymentViewSet

urlpatterns = [
    path("student/fees", StudentFeeViewSet.as_view({"get": "list"})),
    path("student/fees/<int:pk>", StudentFeeViewSet.as_view({"get": "retrieve"})),

    path("student/payments", StudentPaymentViewSet.as_view({"get": "list"})),
    path("student/payments/<int:pk>", StudentPaymentViewSet.as_view({"get": "retrieve"})),
]
