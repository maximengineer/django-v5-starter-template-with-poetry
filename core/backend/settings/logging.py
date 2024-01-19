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
            "filename": "general.log",
            "level": "DEBUG",
            "formatter": "standard",
            "filters": [],
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "filters": [],
        },
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["file", "console"],
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["file", "console"],
    },
}
