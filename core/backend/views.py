import logging

from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit

logger = logging.getLogger(__name__)


@ratelimit(key="ip", rate=settings.RATELIMIT_RATE_DEFAULT, method="GET")
def home_view(request):
    """
    Home page view with rate limiting.
    Rate limit configured in settings.RATELIMIT_RATE_DEFAULT (default: 60/m).
    """
    context = {}
    return render(request, "pages/home.html", context)


@csrf_exempt
@require_http_methods(["GET", "HEAD"])
@ratelimit(key="ip", rate=settings.RATELIMIT_RATE_HEALTH, method="GET")
def health_check(request):
    """
    Health check endpoint for Docker healthcheck and monitoring.

    This endpoint is exempt from CSRF protection because it's used by:
    - Docker healthchecks
    - Load balancers
    - Monitoring systems (Prometheus, Datadog, etc.)

    Rate limit configured in settings.RATELIMIT_RATE_HEALTH (default: 120/m).
    Higher rate limit than normal views to accommodate monitoring systems.
    Only GET and HEAD methods are allowed for security.
    Returns JSON with status and database connectivity.
    """
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

        return JsonResponse(
            {
                "status": "healthy",
                "database": "connected",
                "version": "5.2",
            }
        )
    except Exception as e:
        # Log the error for debugging (includes full traceback)
        logger.error("Health check failed: Database connection error", exc_info=True)

        # Return sanitized error message
        # In DEBUG mode, include error details; in production, keep it generic
        error_detail = str(e) if settings.DEBUG else "Database unavailable"

        return JsonResponse(
            {
                "status": "unhealthy",
                "database": "disconnected",
                "error": error_detail,
            },
            status=503,
        )


def ratelimit_view(request, exception):
    """
    Custom view for rate limit exceeded responses.
    Returns JSON response with 429 status code.
    """
    return JsonResponse(
        {
            "error": "Rate limit exceeded",
            "detail": "Too many requests. Please try again later.",
        },
        status=429,
    )
