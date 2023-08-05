"""
Django settings for 'main' project. Django version: 3.1.

Configuration instructions: https://docs.djangoproject.com/en/3.1/topics/settings/
Deployment Checklist: https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/
"""

import json
import logging
from os import environ
from pathlib import Path
import dj_database_url

from django.core.management.utils import get_random_secret_key
from django.utils.translation import gettext_lazy as _


BASE_DIR = Path(__file__).resolve().parent.parent
LOGGER = logging.getLogger(__name__)
DEBUG = os.environ.get("DEBUG") == "TRUE"

if "SECRET_KEY" not in environ:
    LOGGER.critical("SECRET KEY COULD NOT BE RETRIEVED. GENERATING RANDOM ONE.")
SECRET_KEY = environ.setdefault("SECRET_KEY", get_random_secret_key())

ALLOWED_HOSTS = ["*"]
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True


# Application definition:

ROOT_URLCONF = "main.urls"
WSGI_APPLICATION = "main.wsgi.application"
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
ADMINS = [("ADMIN_1", environ.get("EMAIL_SENDER", ""))]
MANAGERS = ADMINS

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "corsheaders",
    "rest_framework",
    "debug_toolbar",
    "crispy_forms",
    "django_js_reverse",
    # TODO: Add apps here!
]


# Middleware: https://docs.djangoproject.com/en/3.1/topics/http/middleware/#activating-middleware

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# Templates: https://docs.djangoproject.com/en/3.1/topics/templates/#configuration

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


# Database: https://docs.djangoproject.com/en/3.1/ref/settings/#databases
# dj-database-url: https://pypi.org/project/dj-database-url/

DATABASES = {"default": dj_database_url.config(conn_max_age=600, default=f"sqlite:///{BASE_DIR / "db.sqlite3"}")}


# Caches: https://docs.djangoproject.com/en/3.1/topics/cache/

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}


# Password validation: https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Logging: https://docs.djangoproject.com/en/3.1/topics/logging/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
        "debug": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "errors.log",
            "backupCount": 10,
            "maxBytes": 5242880,  # 5MB
            "formatter": "timed",
        },
    },
    "formatters": {
        "timed": {
            "format": "[{asctime}] {message}",
            "style": "{",
        }
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}


# Internationalization: https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "fi-fi"
TIME_ZONE = "Europe/Helsinki"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = [
    ("fi", _("Finnish")),
    ("en", _("English")),
]


# Static files: https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT = BASE_DIR / "media"


# Email settings: https://docs.djangoproject.com/en/3.1/topics/email/

EMAIL_HOST_USER = environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = environ.get("EMAIL_HOST_PASSWORD", "")

EMAIL_HOST = environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = environ.get("EMAIL_PORT", 587)
EMAIL_USE_TLS = environ.get("EMAIL_USE_TLS", True)
EMAIL_USE_SSL = False if EMAIL_USE_TLS else environ.get("EMAIL_USE_SSL", False)
EMAIL_BACKEND = environ.get("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")

EMAIL_SENDER = environ.get("EMAIL_SENDER", "")
EMAIL_SUBJECT_PREFIX = environ.get("EMAIL_SUBJECT_PREFIX", "[main] ")
DEFAULT_FROM_EMAIL = environ.get("DEFAULT_FROM_EMAIL", EMAIL_SENDER)  # e.g. django.contrib.auth
SERVER_EMAIL = environ.get("SERVER_EMAIL", EMAIL_SENDER)  # e.g. server errors


# Third party apps

# Django Crispy Forms: https://django-crispy-forms.readthedocs.io/en/latest/
CRISPY_TEMPLATE_PACK = "bootstrap4"

# Django JS Reverse: https://django-js-reverse.readthedocs.io/en/latest/
JS_REVERSE_JS_VAR_NAME = "reverse"
JS_REVERSE_JS_GLOBAL_OBJECT_NAME = "window"

# Django Rest Framework: https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
}

if DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].insert(0, "rest_framework.renderers.BrowsableAPIRenderer")

CORS_ORIGIN_ALLOW_ALL = DEBUG
if not DEBUG:
    CORS_ALLOWED_ORIGINS = environ.get("CORS_ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000").split(",")


def show_toolbar(request):
    return DEBUG


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}
