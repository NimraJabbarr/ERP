"""
Django settings for the School ERP project.

Secrets and environment-specific values are read from environment variables
(via python-decouple) -- see `.env.example` for the variables you need to set.
"""

import urllib.parse
from pathlib import Path
from datetime import timedelta
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# ── SECURITY ──────────────────────────────────────────────────────────────
SECRET_KEY = config("DJANGO_SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

# Comma-separated extra hosts (your own domain, etc.) + Vercel's domain.
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", default="localhost,127.0.0.1"
).split(",") + [".vercel.app"]

# ── INSTALLED APPS ─────────────────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_yasg",              # Swagger / ReDoc interactive API docs
    "corsheaders",            # allows the React frontend (different origin) to call this API
    "channels",                # WebSocket support, used by the AI chatbot

    # Project apps (domain-organized, NOT role-organized -- see project notes)
    "accounts",
    "academics",
    "attendance",
    "finance",
    "chat",
    "communication",
    "administration",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",   # must sit right after SecurityMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",   # must sit above CommonMiddleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"  # required because Channels handles the WebSocket chatbot

# ── CUSTOM USER MODEL ───────────────────────────────────────────────────────
# Must be set BEFORE the first `migrate` is ever run -- it cannot be
# changed afterwards without rebuilding the database.
AUTH_USER_MODEL = "accounts.User"

# ── DATABASE (Neon Postgres, via a single connection-string env var) ───────
# In Vercel, set DATABASE_URL to your Neon *pooled* connection string
# (the one with "-pooler" in the hostname) -- that's the one safe for
# serverless, since every request can open a fresh connection.
# For local `manage.py migrate` runs, use the *direct* (non -pooler) string.
DATABASE_URL = config("DATABASE_URL", default="")

if DATABASE_URL:
    _db = urllib.parse.urlparse(DATABASE_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": _db.path.lstrip("/"),
            "USER": _db.username,
            "PASSWORD": _db.password,
            "HOST": _db.hostname,
            "PORT": _db.port or 5432,
            "OPTIONS": {"sslmode": "require"},  # Neon requires SSL
        }
    }
else:
    # Local fallback so the project still runs without Neon configured.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ── REST FRAMEWORK + JWT AUTHENTICATION ─────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    # Enforce Admin approval workflow for login/token issuance.
    "TOKEN_OBTAIN_PAIR_SERIALIZER": "accounts.authentication.StatusAwareTokenObtainPairSerializer",
}

# ── SWAGGER (drf-yasg) ──────────────────────────────────────────────────────
# Once running, visit /swagger/ for an interactive UI to test every
# endpoint directly in the browser (no Postman needed), or /redoc/ for a
# clean read-only reference view.
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
    "USE_SESSION_AUTH": False,
}

# ── CORS (allow the React frontend to call this API from a different domain) ──
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS", default="http://localhost:5173"
).split(",")

# ── CHANNELS (WebSocket layer for the AI chatbot, backed by Redis) ──────────
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [config("REDIS_URL", default="redis://localhost:6379/0")]},
    },
}

# ── CELERY (background tasks + scheduled cron jobs, e.g. monthly fee generation) ──
CELERY_BROKER_URL = config("REDIS_URL", default="redis://localhost:6379/0")
CELERY_RESULT_BACKEND = config("REDIS_URL", default="redis://localhost:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Karachi"

# ── PASSWORD VALIDATION ──────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ── INTERNATIONALIZATION ──────────────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Karachi"
USE_I18N = True
USE_TZ = True

# ── STATIC FILES (Vercel runs collectstatic automatically at build time) ────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ── STRIPE (online fee payments -- TEST MODE keys until you go live) ───────
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default="")
STRIPE_PUBLISHABLE_KEY = config("STRIPE_PUBLISHABLE_KEY", default="")
STRIPE_WEBHOOK_SECRET = config("STRIPE_WEBHOOK_SECRET", default="")

FRONTEND_URL = config("FRONTEND_URL", default="http://localhost:5173")

# ── EMAILJS (optional -- safe defaults so the app doesn't crash without it) ─
EMAILJS_SERVICE_ID = config("EMAILJS_SERVICE_ID", default="")
EMAILJS_TEMPLATE_ID = config("EMAILJS_TEMPLATE_ID", default="")
EMAILJS_PUBLIC_KEY = config("EMAILJS_PUBLIC_KEY", default="")
EMAILJS_PRIVATE_KEY = config("EMAILJS_PRIVATE_KEY", default="")

# ── PRODUCTION SECURITY (Vercel terminates SSL for you, sets this header) ──
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=False, cast=bool)
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=False, cast=bool)
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=False, cast=bool)

# ── LOGGING (shows up in Vercel's function logs) ────────────────────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}