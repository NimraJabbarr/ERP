from django.urls import path, include

urlpatterns = [
    path("", include("finance.urls.admin")),
    # finance.urls.others -- /api/finance/my-fees and /api/finance/statement/{id}, built by Dev B
    path("", include("finance.urls.student")),
    path("", include("finance.urls.teacher")),
    path("", include("finance.urls.parent")),
]