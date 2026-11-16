"""Independent DeltaDevelop studio; credentials are environment-only."""
import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = os.getenv("DJANGO_DEBUG", "0") == "1"
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "")
if not SECRET_KEY and DEBUG:
    SECRET_KEY = "local-debug-only-never-use-on-server"
if not SECRET_KEY:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY must be set in production.")

ALLOWED_HOSTS = [v.strip() for v in os.getenv(
    "DJANGO_ALLOWED_HOSTS", "deltadevelop.ir,www.deltadevelop.ir,localhost,127.0.0.1"
).split(",") if v.strip()]
CSRF_TRUSTED_ORIGINS = [v.strip() for v in os.getenv(
    "DJANGO_CSRF_TRUSTED_ORIGINS", "https://deltadevelop.ir,https://www.deltadevelop.ir"
).split(",") if v.strip()]

INSTALLED_APPS = [
    "django.contrib.admin", "django.contrib.auth",
    "django.contrib.contenttypes", "django.contrib.sessions",
    "django.contrib.messages", "django.contrib.staticfiles",
    "studio.apps.StudioConfig",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
        "studio.context.studio_context",
    ]},
}]
WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {"default": dj_database_url.config(
    default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}", conn_max_age=60,
)}
LANGUAGE_CODE = "fa-ir"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STORAGES = {"staticfiles": {
    "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
}}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = os.getenv("DJANGO_SECURE_SSL_REDIRECT", "0") == "1"
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024
