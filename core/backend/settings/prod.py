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

# Security Settings - Enable in production
# Note: Disabled for local testing. Enable these for actual production deployment:
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") if env.bool("USE_HTTPS", default=False) else None

# HSTS Settings
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False)
SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD", default=False)

# Cookie Security
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=False)
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=False)

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# Redis Cache Configuration (if REDIS_URL is set)
redis_url = env("REDIS_URL", default=None)
if redis_url:
    CACHES = {  # noqa: F405
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": redis_url,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "SOCKET_CONNECT_TIMEOUT": 5,
                "SOCKET_TIMEOUT": 5,
                "CONNECTION_POOL_KWARGS": {
                    "max_connections": 50,
                    "retry_on_timeout": True,
                },
            },
            "KEY_PREFIX": "django",
        }
    }

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
