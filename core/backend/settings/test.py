"""Test settings."""
from .base import *  # noqa: F403, F401

# Test SECRET_KEY (never use in production!)
SECRET_KEY = "django-insecure-test-key-for-testing-only-do-not-use-in-production"

# Use in-memory SQLite database for tests to speed up execution
DATABASES = {  # noqa: F405
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

DEBUG = True

# Colored logging for test output
LOGGING["formatters"]["colored"] = {  # noqa: F405
    "()": "colorlog.ColoredFormatter",
    "format": "%(log_color)s%(asctime)s %(levelname)s %(name)s %(bold_white)s%(message)s",
}

# Set debug logging for tests
LOGGING["root"]["level"] = "DEBUG"  # noqa: F405
LOGGING["handlers"]["console"]["level"] = "DEBUG"  # noqa: F405
LOGGING["handlers"]["console"]["formatter"] = "colored"  # noqa: F405
