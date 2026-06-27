from django.urls import path
from finance.views.parent import ParentFeeViewSet, ParentPaymentViewSet

urlpatterns = [
    path("parent/fees", ParentFeeViewSet.as_view({"get": "list"})),
    path("parent/fees/<int:pk>", ParentFeeViewSet.as_view({"get": "retrieve"})),

    path("parent/payments", ParentPaymentViewSet.as_view({"get": "list"})),
    path("parent/payments/<int:pk>", ParentPaymentViewSet.as_view({"get": "retrieve"})),
]
