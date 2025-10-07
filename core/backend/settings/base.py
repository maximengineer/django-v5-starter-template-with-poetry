from pathlib import Path
import environ

# Initialize environment variables
env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# Note: When using split-settings, BASE_DIR might already be defined in __init__.py
#  __file__ points to this file: core/backend/settings/base.py
#  We need to go up 4 levels to reach project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

DEBUG = False

SECRET_KEY = NotImplemented

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "corsheaders",
    "rest_framework",
    "drf_spectacular",
    "django_filters",
    "django_extensions",
    # Project apps
    "core.backend.apps.BackendConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "core" / "templates"],
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

WSGI_APPLICATION = "core.backend.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", default="backend_db"),
        "USER": env("POSTGRES_USER", default="backend_user"),
        "PASSWORD": env("POSTGRES_PASSWORD", default="backend_password"),
        "HOST": env("POSTGRES_HOST", default="localhost"),
        "PORT": env("POSTGRES_PORT", default="5432"),
        "ATOMIC_REQUESTS": True,
        "CONN_MAX_AGE": 600,  # Keep connections alive for 10 minutes
        "CONN_HEALTH_CHECKS": True,  # Validate connections before reuse
    }
}

# Note: Django 5.2+ supports connection pooling via OPTIONS["pool"], but it's
# incompatible with CONN_MAX_AGE (persistent connections). For a starter template,
# persistent connections (CONN_MAX_AGE) are recommended as they're simpler and
# work well for most applications.
#
# To enable connection pooling instead (for high-traffic applications):
# 1. Remove or set CONN_MAX_AGE to 0
# 2. Install psycopg[pool]: poetry add "psycopg[pool]"
# 3. Add OPTIONS: {"pool": {"min_size": 2, "max_size": 10}}
# See: https://docs.djangoproject.com/en/5.2/ref/databases/#postgresql-connection-pooling

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_URL = "static/"
# STATICFILES_DIRS: Not needed - Django apps will use their own static/ directories
# WhiteNoise serves files from STATIC_ROOT after collectstatic
STATIC_ROOT = BASE_DIR / "local-cdn" / "static"

# Media files (User uploads)
# https://docs.djangoproject.com/en/5.2/topics/files/
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Django 4.2+ STORAGES setting
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": MEDIA_ROOT,
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS Configuration
# https://github.com/adamchainz/django-cors-headers
# Default: Restrictive settings for security
# Override in dev.py with CORS_ALLOW_ALL_ORIGINS = True
# Override in prod.py with specific origins
CORS_ALLOWED_ORIGINS = []  # Empty = no origins allowed (override in environment settings)
CORS_ALLOW_CREDENTIALS = False  # Disabled by default (enable in prod with specific origins)

# Django REST Framework
REST_FRAMEWORK = {
    # Pagination
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
    # Authentication
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    # Permissions
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    # Rendering
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    # Filtering
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    # Throttling
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
    },
    # Versioning
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1"],
    # Exception handling
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
    # Schema - Use drf-spectacular for OpenAPI 3.0
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# drf-spectacular settings
SPECTACULAR_SETTINGS = {
    "TITLE": "Django 5.2 Starter API",
    "DESCRIPTION": "API documentation for Django 5.2 starter template with DRF",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": "/api/",
}

# Caching Configuration
# Default: Local memory cache (no Redis required)
# Production: Set REDIS_URL environment variable to use Redis
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# Django Ratelimit Configuration
# https://django-ratelimit.readthedocs.io/
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = "default"  # Uses Django's cache backend
RATELIMIT_VIEW = "core.backend.views.ratelimit_view"  # Custom view for rate limit exceeded

# Centralized rate limit defaults (can be overridden in views)
# Format: "number/period" where period is s(econd), m(inute), h(our), d(ay)
RATELIMIT_RATE_DEFAULT = "60/m"  # Default: 60 requests per minute
RATELIMIT_RATE_API = "100/m"  # API endpoints: 100 requests per minute
RATELIMIT_RATE_HEALTH = "120/m"  # Health checks: 120 requests per minute (higher for monitoring)

# ==============================================================================
# LOGGING
# ==============================================================================

import environ

env = environ.Env()

# Log file location
LOG_FILE = BASE_DIR / "logs" / "django.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "{asctime} - {levelname} - {name} : {message}",
            "style": "{",
        },
        "verbose": {
            "format": "{asctime} - {levelname} - {name} - {module}.py (line {lineno:d}) : {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": str(LOG_FILE),
            "formatter": "standard",
            "level": "INFO",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],
    },
    "loggers": {
        "django": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "core": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },
}

# ==============================================================================
# SECURITY
# ==============================================================================

# HTTPS/SSL (disabled by default for development, enable in production)
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# HSTS (disabled by default, enable in production settings)
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Cookie Security
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = []  # Add ['https://yourdomain.com'] in production

# Security Headers
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
# Note: SECURE_BROWSER_XSS_FILTER removed (deprecated in Django 4.0+)
