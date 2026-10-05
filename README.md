<div align="center">

# 🎓 School Assistant — School ERP System

### A complete backend for managing schools — students, parents, teachers, and admins — in one place.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-REST%20Framework-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-API-red)](https://www.django-rest-framework.org/)
[![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?logo=vercel)](https://vercel.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📖 About

**School Assistant** is a REST API backend for a full-featured **School ERP (Enterprise Resource Planning) system**. It handles everything a school needs — from managing students, parents, and teachers to tracking attendance, running a chat system, handling finances, and keeping communication flowing between all parties.

The system is built around **four user roles**, each with their own permissions and views:

| Role | What They Can Do |
|------|------------------|
| 👨‍🎓 **Student** | View their own attendance, marks, fees, notices, and chat with teachers |
| 👨‍👩‍👧 **Parent** | Track their child's attendance, performance, fees, and communicate with teachers |
| 👩‍🏫 **Teacher** | Manage classes, mark attendance, upload marks, chat with students/parents |
| 🛡️ **Admin** | Full control — manage users, fees, classes, notices, and system configuration |

---

## ✨ Features

### 🔐 Accounts & Authentication
- Custom user model with role-based access (Student / Parent / Teacher / Admin)
- JWT-style token authentication
- Role-based permissions (`permissions.py`)
- Separate serializers for registration, login, and profile

### 📚 Academics
- Manage classes, sections, and subjects
- Assign teachers to subjects
- Store and retrieve marks/grades per student
- Class-wise and student-wise academic records

### 📋 Attendance
- Daily attendance tracking by teacher
- Student-wise and class-wise attendance history
- Attendance reports for parents
- Leave request handling

### 💰 Finance
- Fee structure management
- Fee collection tracking
- Payment history per student
- Outstanding dues and reminders

### 💬 Chat
- Real-time (or near real-time) chat between roles
- Teacher ↔ Student chat
- Teacher ↔ Parent chat
- Admin broadcast messaging

### 📢 Communication
- Notice board / announcements
- Circulars for specific classes or the whole school
- Event notifications

### 🛡️ Administration
- Admin dashboard endpoints
- User management (create/update/deactivate)
- System configuration
- Reports and analytics

### ⚙️ Config
- Central project settings
- Environment-based configuration
- Database and app-level settings

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.10+** | Core language |
| **Django** | Web framework |
| **Django REST Framework** | REST API layer |
| **SQLite / PostgreSQL** | Database |
| **Vercel** | Deployment |
| **Gunicorn** | WSGI server (production) |
| **WhiteNoise** | Static file serving |

---

## 📁 Project Structure

```text
school_assistant/
│
├── school_assistant/              # Django project root
│   │
│   ├── accounts/                  # Users, auth, roles, permissions
│   │   ├── migrations/
│   │   ├── serializers/
│   │   ├── urls/
│   │   ├── views/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── authentication.py
│   │   └── permissions.py
│   │
│   ├── academics/                 # Classes, subjects, marks
│   │   ├── migrations/
│   │   ├── serializers/
│   │   ├── urls/
│   │   ├── views/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   └── models.py
│   │
│   ├── administration/            # Admin panel logic
│   ├── attendance/                # Attendance tracking
│   ├── chat/                      # Messaging between roles
│   ├── communication/             # Notices & announcements
│   ├── config/                    # Shared configuration
│   └── finance/                   # Fees & payments
│
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── runtime.txt                    # Python runtime version (for deployment)
├── Procfile                       # Process file for deployment
├── vercel.json                    # Vercel deployment config
├── .gitignore
└── README.md
