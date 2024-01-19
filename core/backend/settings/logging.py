import environ

from core.backend.settings import BASE_DIR

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env(BASE_DIR / ".env")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "{asctime} - {levelname} - {name} : {message}",
            "style": "{",
        },
        "verbose": {
            "format": "{asctime} - {levelname} - {name} - {module}.py - (line {lineno:d}) : {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": env("DJANGO_LOG_FILE"),
            "level": env("DJANGO_LOG_LEVEL"),
            "formatter": "standard",
            "filters": [],
        },
        "console": {
            "level": env("DJANGO_LOG_LEVEL"),
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "filters": [],
        },
    },
    "loggers": {
        "": {
            "level": env("DJANGO_LOG_LEVEL"),
            "handlers": ["file", "console"],
        }
    },
    "root": {
        "level": env("DJANGO_LOG_LEVEL"),
        "handlers": ["file", "console"],
    },
}
