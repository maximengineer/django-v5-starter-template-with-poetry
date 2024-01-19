# Example settings to be used in local/settings.dev.py
from core.backend.settings.logging import LOGGING

SECRET_KEY = ""

DEBUG = True

# colored formatter use for console only
LOGGING["formatters"]["colored"] = {
    "()": "colorlog.ColoredFormatter",
    "format": "%(log_color)s%(asctime)s %(levelname)s %(name)s %(bold_white)s%(message)s",
}

LOGGING["loggers"][""]["level"] = "DEBUG"

LOGGING["handlers"]["file"]["level"] = "DEBUG"
LOGGING["handlers"]["file"]["formatter"] = "standard"

LOGGING["handlers"]["console"]["level"] = "DEBUG"
LOGGING["handlers"]["console"]["formatter"] = "colored"
