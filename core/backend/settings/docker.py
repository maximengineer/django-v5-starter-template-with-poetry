from core.backend.settings.base import MIDDLEWARE
from core.backend.settings.custom import IN_DOCKER

if IN_DOCKER:
    assert MIDDLEWARE[:1] == [
        "django.middleware.security.SecurityMiddleware",
    ]
