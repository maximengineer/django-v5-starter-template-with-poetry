"""
Custom Django system checks for security and configuration validation.
These checks run automatically with `python manage.py check` and during deployment.
"""

from django.core.checks import Error, Warning, register, Tags
from django.conf import settings


@register(Tags.security)
def check_secret_key_strength(app_configs, **kwargs):
    """
    Check that SECRET_KEY is strong enough for production.
    """
    errors = []

    if not settings.SECRET_KEY or settings.SECRET_KEY == NotImplemented:
        errors.append(
            Error(
                "SECRET_KEY is not set",
                hint="Set SECRET_KEY in your settings or environment variables",
                id="security.E001",
            )
        )
    elif len(settings.SECRET_KEY) < 50:
        errors.append(
            Error(
                "SECRET_KEY is too short",
                hint="Use at least 50 characters for SECRET_KEY",
                id="security.E002",
            )
        )
    elif settings.SECRET_KEY == "django-insecure-change-this-in-production":
        errors.append(
            Error(
                "SECRET_KEY is using default insecure value",
                hint="Generate a new SECRET_KEY for production",
                id="security.E003",
            )
        )

    return errors


@register(Tags.security)
def check_debug_in_production(app_configs, **kwargs):
    """
    Check that DEBUG is False in production.
    """
    errors = []

    if not settings.DEBUG:
        # Production mode - check for proper configuration
        if not settings.ALLOWED_HOSTS:
            errors.append(
                Error(
                    "ALLOWED_HOSTS is empty in production (DEBUG=False)",
                    hint="Set ALLOWED_HOSTS to your domain(s)",
                    id="security.E004",
                )
            )

    return errors


@register(Tags.security)
def check_security_middleware(app_configs, **kwargs):
    """
    Check that critical security middleware is installed.
    """
    warnings = []

    required_middleware = [
        "django.middleware.security.SecurityMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    for middleware in required_middleware:
        if middleware not in settings.MIDDLEWARE:
            warnings.append(
                Warning(
                    f"Missing security middleware: {middleware}",
                    hint=f"Add '{middleware}' to MIDDLEWARE setting",
                    id="security.W001",
                )
            )

    return warnings


@register(Tags.database)
def check_sqlite_in_production(app_configs, **kwargs):
    """
    Check that SQLite is not used in production.
    """
    errors = []

    if not settings.DEBUG:
        # Check if using SQLite in production
        db_engine = settings.DATABASES.get("default", {}).get("ENGINE", "")
        if "sqlite" in db_engine:
            errors.append(
                Error(
                    "SQLite database is used in production (DEBUG=False)",
                    hint="Use PostgreSQL, MySQL, or another production database",
                    id="database.E001",
                )
            )

    return errors


@register(Tags.caches)
def check_cache_configuration(app_configs, **kwargs):
    """
    Check cache configuration and recommend Redis for production.
    """
    warnings = []

    if not settings.DEBUG:
        # Check if using local memory cache in production
        cache_backend = settings.CACHES.get("default", {}).get("BACKEND", "")
        if "locmem" in cache_backend.lower() or "dummycache" in cache_backend.lower():
            warnings.append(
                Warning(
                    "Using local memory cache in production",
                    hint="Consider using Redis cache for better performance in production",
                    id="caches.W001",
                )
            )

    return warnings
