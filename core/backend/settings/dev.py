"""Development settings."""
from .base import *  # noqa: F403, F401
import environ
import sys

env = environ.Env()

# Development SECRET_KEY
# Best practice: Set in .env file to avoid sharing keys between developers
# If not set, falls back to insecure default (with warning)
SECRET_KEY = env(
    "SECRET_KEY",
    default="django-insecure-y87e+4vt0b040c7_d2snx&@n1mf91#!1ose!ieimfgl2s9+*ev"
)

# Warn if using default SECRET_KEY
if SECRET_KEY == "django-insecure-y87e+4vt0b040c7_d2snx&@n1mf91#!1ose!ieimfgl2s9+*ev":
    print(
        "\n⚠️  WARNING: Using default development SECRET_KEY!\n"
        "   This is insecure if multiple developers use the same key.\n"
        "   Set a unique SECRET_KEY in your .env file:\n"
        "     SECRET_KEY='django-insecure-<your-unique-key-here>'\n"
        "   Generate one with:\n"
        "     python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'\n",
        file=sys.stderr
    )

# Enable debug mode
DEBUG = True

# Allow all hosts in development
ALLOWED_HOSTS = ["*"]

# CORS - Allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True

# Django Debug Toolbar
INSTALLED_APPS += [  # noqa: F405
    "debug_toolbar",
]

MIDDLEWARE = [  # noqa: F405
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE  # noqa: F405

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

# Debug Toolbar Configuration
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
}

# Colored logging for development
LOGGING["formatters"]["colored"] = {  # noqa: F405
    "()": "colorlog.ColoredFormatter",
    "format": "%(log_color)s%(asctime)s - %(levelname)s - %(name)s - %(bold_white)s%(message)s",
}

LOGGING["root"]["level"] = "DEBUG"  # noqa: F405
LOGGING["handlers"]["console"]["level"] = "DEBUG"  # noqa: F405
LOGGING["handlers"]["console"]["formatter"] = "colored"  # noqa: F405
