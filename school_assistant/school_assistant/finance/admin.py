from django.contrib import admin
from .models import (
    FeeStructure,
    Fee,
    Payment,
    Expense,
    FeeHistory,
)

admin.site.register(FeeStructure)
admin.site.register(Fee)
admin.site.register(Payment)
admin.site.register(Expense)
admin.site.register(FeeHistory)