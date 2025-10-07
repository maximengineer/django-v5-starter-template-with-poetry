import pytest
from django.test import Client, override_settings
from django.urls import reverse
from unittest.mock import patch

pytestmark = pytest.mark.django_db


# Health Check Tests
def test_health_check_success():
    """
    GIVEN a Django client with working database
    WHEN the /health/ endpoint is requested
    THEN the response should be 200 OK with healthy status
    """
    client = Client()
    url = reverse("health_check")
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert "version" in data


def test_health_check_database_error():
    """
    GIVEN a Django client with database connection error
    WHEN the /health/ endpoint is requested
    THEN the response should be 503 with error details
    """
    client = Client()
    url = reverse("health_check")

    # Mock database error
    with patch("django.db.connection.cursor") as mock_cursor:
        mock_cursor.side_effect = Exception("Database connection failed")
        response = client.get(url)

    assert response.status_code == 503
    data = response.json()
    assert data["status"] == "unhealthy"
    assert data["database"] == "disconnected"
    assert "error" in data


def test_health_check_head_method():
    """
    GIVEN a Django client
    WHEN the /health/ endpoint is requested with HEAD method
    THEN the response should be 200 OK
    """
    client = Client()
    url = reverse("health_check")
    response = client.head(url)

    assert response.status_code == 200


def test_health_check_post_not_allowed():
    """
    GIVEN a Django client
    WHEN the /health/ endpoint is requested with POST method
    THEN the response should be 405 Method Not Allowed
    """
    client = Client()
    url = reverse("health_check")
    response = client.post(url)

    assert response.status_code == 405


# Home View Tests
def test_home_view_success():
    """
    GIVEN a Django client
    WHEN the home page is requested
    THEN the response should be 200 OK with rendered template
    """
    client = Client()
    url = reverse("home")
    response = client.get(url)

    assert response.status_code == 200
    assert "text/html" in response["Content-Type"]


def test_home_view_template_rendering():
    """
    GIVEN a Django client
    WHEN the home page is requested
    THEN the correct template should be rendered
    """
    client = Client()
    url = reverse("home")
    response = client.get(url)

    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.content


# Rate Limiting Tests
# Note: Rate limiting tests require proper cache backend configuration
# These tests are skipped in favor of integration tests
# TODO: Add integration tests for rate limiting with Redis backend


# Error Response Tests
@override_settings(DEBUG=True)
def test_health_check_error_debug_mode():
    """
    GIVEN DEBUG mode is enabled
    WHEN the /health/ endpoint encounters an error
    THEN the response should include detailed error message
    """
    client = Client()
    url = reverse("health_check")

    with patch("django.db.connection.cursor") as mock_cursor:
        mock_cursor.side_effect = Exception("Detailed error message")
        response = client.get(url)

    data = response.json()
    assert "Detailed error message" in data["error"]


@override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"])
def test_health_check_error_production_mode():
    """
    GIVEN DEBUG mode is disabled (production)
    WHEN the /health/ endpoint encounters an error
    THEN the response should have sanitized error message
    """
    client = Client()
    url = reverse("health_check")

    with patch("django.db.connection.cursor") as mock_cursor:
        mock_cursor.side_effect = Exception("Detailed error message")
        response = client.get(url)

    data = response.json()
    assert data["error"] == "Database unavailable"
    assert "Detailed error message" not in data["error"]
