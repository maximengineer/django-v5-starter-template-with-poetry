"""Tests for custom Django system checks."""
import pytest
from django.conf import settings
from django.core.checks import Error, Warning
from django.test import override_settings

from core.backend.checks import (
    check_secret_key_strength,
    check_debug_in_production,
    check_security_middleware,
    check_sqlite_in_production,
    check_cache_configuration,
)


class TestSecretKeyChecks:
    """Tests for SECRET_KEY strength validation."""

    @override_settings(SECRET_KEY="too-short")
    def test_short_secret_key(self):
        """SECRET_KEY shorter than 50 characters should raise error."""
        errors = check_secret_key_strength(app_configs=None)
        assert len(errors) == 1
        assert errors[0].id == "security.E002"
        assert "too short" in errors[0].msg

    @override_settings(SECRET_KEY="a" * 50)
    def test_valid_secret_key(self):
        """Valid SECRET_KEY should pass."""
        errors = check_secret_key_strength(app_configs=None)
        assert len(errors) == 0


class TestDebugProductionChecks:
    """Tests for DEBUG mode validation."""

    @override_settings(DEBUG=False, ALLOWED_HOSTS=[])
    def test_production_empty_allowed_hosts(self):
        """Empty ALLOWED_HOSTS in production should raise error."""
        errors = check_debug_in_production(app_configs=None)
        assert len(errors) == 1
        assert errors[0].id == "security.E004"
        assert "ALLOWED_HOSTS is empty" in errors[0].msg

    @override_settings(DEBUG=False, ALLOWED_HOSTS=["example.com"])
    def test_production_with_allowed_hosts(self):
        """Production with ALLOWED_HOSTS should pass."""
        errors = check_debug_in_production(app_configs=None)
        assert len(errors) == 0

    @override_settings(DEBUG=True, ALLOWED_HOSTS=[])
    def test_development_empty_allowed_hosts(self):
        """Empty ALLOWED_HOSTS in development should pass."""
        errors = check_debug_in_production(app_configs=None)
        assert len(errors) == 0


class TestSecurityMiddlewareChecks:
    """Tests for security middleware validation."""

    def test_missing_security_middleware(self):
        """Missing SecurityMiddleware should raise warning."""
        with override_settings(MIDDLEWARE=[]):
            warnings = check_security_middleware(app_configs=None)
            assert len(warnings) == 3  # 3 required middleware missing
            assert all(isinstance(w, Warning) for w in warnings)
            assert any(w.id == "security.W001" for w in warnings)

    def test_all_security_middleware_present(self):
        """All security middleware present should pass."""
        middleware = [
            "django.middleware.security.SecurityMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ]
        with override_settings(MIDDLEWARE=middleware):
            warnings = check_security_middleware(app_configs=None)
            assert len(warnings) == 0


class TestDatabaseChecks:
    """Tests for database configuration validation."""

    @override_settings(
        DEBUG=False,
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3"}}
    )
    def test_sqlite_in_production(self):
        """SQLite in production should raise error."""
        errors = check_sqlite_in_production(app_configs=None)
        assert len(errors) == 1
        assert errors[0].id == "database.E001"
        assert "SQLite" in errors[0].msg

    @override_settings(
        DEBUG=False,
        DATABASES={"default": {"ENGINE": "django.db.backends.postgresql"}}
    )
    def test_postgresql_in_production(self):
        """PostgreSQL in production should pass."""
        errors = check_sqlite_in_production(app_configs=None)
        assert len(errors) == 0

    @override_settings(
        DEBUG=True,
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3"}}
    )
    def test_sqlite_in_development(self):
        """SQLite in development should pass."""
        errors = check_sqlite_in_production(app_configs=None)
        assert len(errors) == 0


class TestCacheChecks:
    """Tests for cache configuration validation."""

    @override_settings(
        DEBUG=False,
        CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
    )
    def test_locmem_cache_in_production(self):
        """Local memory cache in production should raise warning."""
        warnings = check_cache_configuration(app_configs=None)
        assert len(warnings) == 1
        assert warnings[0].id == "caches.W001"
        assert "local memory cache" in warnings[0].msg.lower()

    @override_settings(
        DEBUG=False,
        CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
    )
    def test_dummy_cache_in_production(self):
        """Dummy cache in production should raise warning."""
        warnings = check_cache_configuration(app_configs=None)
        assert len(warnings) == 1
        assert warnings[0].id == "caches.W001"

    @override_settings(
        DEBUG=False,
        CACHES={"default": {"BACKEND": "django.core.cache.backends.redis.RedisCache"}}
    )
    def test_redis_cache_in_production(self):
        """Redis cache in production should pass."""
        warnings = check_cache_configuration(app_configs=None)
        assert len(warnings) == 0

    @override_settings(
        DEBUG=True,
        CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
    )
    def test_locmem_cache_in_development(self):
        """Local memory cache in development should pass."""
        warnings = check_cache_configuration(app_configs=None)
        assert len(warnings) == 0
