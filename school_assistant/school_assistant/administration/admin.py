from django.contrib import admin
from .models import (
    Complaint,
    Inventory,
    SchoolEvent,
    EventParticipation,
    Certificate,
)

admin.site.register(Complaint)
admin.site.register(Inventory)
admin.site.register(SchoolEvent)
admin.site.register(EventParticipation)
admin.site.register(Certificate)