# Example settings to be used in local/settings.dev.py
import environ

from core.backend.settings import BASE_DIR
from core.backend.settings.logging import LOGGING

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = "django-insecure-y87e+4vt0b040c7_d2snx&@n1mf91#!1ose!ieimfgl2s9+*ev"

DEBUG = True

# colored formatter use for console only
LOGGING["formatters"]["colored"] = {
    "()": "colorlog.ColoredFormatter",
    "format": "%(log_color)s%(asctime)s - %(levelname)s - %(name)s - %(bold_white)s%(message)s",
}

LOGGING["loggers"][""]["level"] = env("DJANGO_LOG_LEVEL")

LOGGING["handlers"]["file"]["level"] = env("DJANGO_LOG_LEVEL")
LOGGING["handlers"]["file"]["formatter"] = "verbose"

LOGGING["handlers"]["console"]["level"] = env("DJANGO_LOG_LEVEL")
LOGGING["handlers"]["console"]["formatter"] = "colored"
