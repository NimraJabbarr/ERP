"""
Celery application instance -- handles background tasks (e.g. WhatsApp
notification dispatch) and scheduled cron jobs (e.g. monthly fee challan
generation), backed by Redis as both the broker and result store.

Run the worker with:
    celery -A config worker -l info

Run the beat scheduler (needed for cron-style periodic tasks) with:
    celery -A config beat -l info
"""

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("school_erp")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Automatically discover a tasks.py file inside each installed app.
app.autodiscover_tasks()
