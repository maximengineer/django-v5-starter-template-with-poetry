"""
AppConfig for the backend application.
"""

from django.apps import AppConfig


class BackendConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.backend"

    def ready(self):
        """
        Called when Django starts.
        Use this to perform initialization tasks.
        """
        # Import and configure admin site
        from django.contrib import admin

        admin.site.site_header = "Django 5.2 Starter Admin"
        admin.site.site_title = "Admin Portal"
        admin.site.index_title = "Welcome to Django 5.2 Starter"

        # Import custom system checks
        from core.backend import checks  # noqa: F401
