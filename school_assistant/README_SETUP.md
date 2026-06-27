# School ERP Backend — Setup Guide

This is the Django backend for the School ERP project: 7 domain-organized
apps (`accounts`, `academics`, `attendance`, `finance`, `chat`,
`communication`, `administration`), 29 models total. Migrations are
already generated and verified — you can `migrate` straight away once
Postgres is configured.

> Views and serializers are NOT included yet — only the schema (models +
> migrations) and project configuration. Build views/serializers on top of
> this once ready, organized by role as already discussed.

---

## 1. Prerequisites

Install on your machine before starting:
- **Python 3.11+**
- **PostgreSQL** (running locally, or a connection string to a hosted instance)
- **Redis** (used by both Celery and Channels/WebSocket)

---

## 2. Create a virtual environment

```bash
cd school_erp_backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in real values — at minimum `DJANGO_SECRET_KEY` and
your actual Postgres credentials (`DB_NAME`, `DB_USER`, `DB_PASSWORD`).

Generate a secret key quickly:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 5. Create the Postgres database

```bash
createdb school_erp          # or use psql / pgAdmin to create it manually
```

## 6. Run migrations

Migrations are already written and tested — this just applies them:

```bash
python manage.py migrate
```

## 7. Seed the 4 Role rows ⚠️ REQUIRED before creating any user

The custom `User` model requires a `Role` foreign key, so the 4 roles must
exist in the database before you register or create anyone — including
the superuser in the next step. Run this once:

```bash
python manage.py shell
```
```python
from accounts.models import Role
Role.objects.bulk_create([
    Role(role_name="Admin", description="System owner"),
    Role(role_name="Teacher"),
    Role(role_name="Student"),
    Role(role_name="Parent"),
])
exit()
```

## 8. Create the Admin (superuser) account

Per the spec, Admin is a single pre-set account with no public signup flow:

```bash
python manage.py createsuperuser
```
You'll be prompted for email, full name, and role — type `1` (or whichever
ID the `Admin` row got in step 7) when asked for the role.

## 9. Run the development server

```bash
python manage.py runserver
```

## 10. Open Swagger for interactive API testing

Once views/serializers/urls are added for each app, visit:
```
http://localhost:8000/swagger/
```
to test every endpoint directly from the browser (no Postman needed), or
```
http://localhost:8000/redoc/
```
for a clean read-only reference view.

---

## 11. Background workers (only needed once chatbot/automation tasks are built)

In separate terminals:

```bash
# Celery worker — runs background tasks (e.g. WhatsApp dispatch)
celery -A config worker -l info

# Celery beat — runs scheduled cron jobs (e.g. monthly fee generation)
celery -A config beat -l info
```

Both require Redis to be running (`redis-server`).

---

## Project structure recap

```
school_erp_backend/
├── manage.py
├── requirements.txt
├── .env.example
├── config/                  # project-level settings, urls, asgi/wsgi, celery
├── accounts/                # Role, User, Student/Teacher/Parent profiles, ParentStudentLink
├── academics/                # ClassSection, Subject, Room, Timetable, Grade, Assignment, AssignmentSubmission
├── attendance/                # Attendance, BehaviorLog
├── finance/                    # FeeStructure, Fee, Payment, Expense, FeeHistory
├── chat/                        # ChatSession, ChatMessage (AI chatbot persistence layer)
├── communication/                # Notification, MediaCampaignLog
└── administration/                # Complaint, Inventory, SchoolEvent, EventParticipation, Certificate
```

## Next steps (not included in this delivery)

1. Build `serializers/` and `views/` per app, split by role (`admin.py`,
   `teacher.py`, `student.py`, `parent.py`) as already discussed, to keep
   the two backend developers' work conflict-free.
2. Build `chat/consumers.py` + `chat/routing.py` for the WebSocket layer,
   then wire it into `config/asgi.py` (marked with a `TODO` there).
3. Build `core/permissions.py` with `IsAdmin`, `IsTeacher`, `IsStudent`,
   `IsParent` classes — shared, write once, both developers import from it.
4. Build Celery tasks (`tasks.py` per app) for monthly fee generation and
   WhatsApp dispatch
