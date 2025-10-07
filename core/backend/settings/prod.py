"""Production settings - override in local deployment."""
from .base import *  # noqa: F403, F401
import environ
import sys

env = environ.Env()

# SECURITY WARNING: keep the secret key used in production secret!
try:
    SECRET_KEY = env("SECRET_KEY")
except environ.ImproperlyConfigured:
    print(
        "\n❌ ERROR: SECRET_KEY environment variable is required for production!\n"
        "Set it in your .env file or environment:\n"
        "  export SECRET_KEY='your-secret-key-here'\n"
        "\nGenerate a secure key with:\n"
        "  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'\n",
        file=sys.stderr
    )
    sys.exit(1)

# Validate SECRET_KEY strength
if len(SECRET_KEY) < 50:
    print(
        f"\n⚠️  WARNING: SECRET_KEY is too short ({len(SECRET_KEY)} characters)!\n"
        f"Production SECRET_KEY should be at least 50 characters for security.\n"
        f"Generate a new one with:\n"
        f"  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'\n",
        file=sys.stderr
    )
    sys.exit(1)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Add your production domain(s)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# Validate ALLOWED_HOSTS is set
if not ALLOWED_HOSTS:
    print(
        "\n⚠️  WARNING: ALLOWED_HOSTS is empty in production!\n"
        "Set it in your .env file or environment:\n"
        "  export ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com'\n",
        file=sys.stderr
    )
    sys.exit(1)

# Security Settings - Enable in production
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# HSTS Settings
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookie Security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# Production logging (console only for Docker/cloud)
LOGGING = {  # noqa: F405
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
