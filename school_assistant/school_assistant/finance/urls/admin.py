from django.urls import path

from finance.views.admin import (
    FeeStructureViewSet, FeeViewSet, GenerateMonthlyChallansView,
    PaymentCreateView, PaymentListView, ExpenseViewSet, FeeHistoryListView,
    CreateStripePaymentIntentView, StripeWebhookView,
)

urlpatterns = [
    path("admin/fee-structures", FeeStructureViewSet.as_view({"get": "list", "post": "create"})),
    path("admin/fee-structures/<int:pk>", FeeStructureViewSet.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
    )),

    path("finance/challans", FeeViewSet.as_view({"get": "list", "post": "create"})),
    path("finance/challans/<int:pk>", FeeViewSet.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
    )),
    path("finance/generate-monthly-challans", GenerateMonthlyChallansView.as_view()),

    path("finance/payments", PaymentCreateView.as_view()),
    path("finance/payments/<int:fee_id>", PaymentListView.as_view()),

    path("admin/expenses", ExpenseViewSet.as_view({"get": "list", "post": "create"})),
    path("admin/expenses/<int:pk>", ExpenseViewSet.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
    )),

    path("finance/fee-history/<int:fee_id>", FeeHistoryListView.as_view()),

    # Stripe
    path("finance/stripe/create-payment-intent", CreateStripePaymentIntentView.as_view()),
    path("finance/stripe/webhook", StripeWebhookView.as_view()),
]