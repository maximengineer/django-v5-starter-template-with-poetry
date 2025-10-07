"""
Django settings router.

Set DJANGO_SETTINGS_MODULE to one of:
- core.backend.settings.dev (default)
- core.backend.settings.prod
- core.backend.settings.test

Or use the shortcut: set DJANGO_ENV=prod and this will route to the correct module.
"""
import os

# Allow shortcut: DJANGO_ENV=prod instead of full module path
env = os.environ.get("DJANGO_ENV", "dev")

if env == "prod":
    from .prod import *  # noqa: F403, F401
elif env == "test":
    from .test import *  # noqa: F403, F401
else:  # dev is default
    from .dev import *  # noqa: F403, F401
