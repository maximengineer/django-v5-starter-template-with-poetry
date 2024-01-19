import os.path
from pathlib import Path

from split_settings.tools import include, optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

ENV_VAR_SETTINGS_PREFIX = "BACKEND_SETTINGS_"

LOCAL_SETTINGS_PATH = os.getenv(f"{ENV_VAR_SETTINGS_PREFIX}LOCAL_SETTINGS")

if not LOCAL_SETTINGS_PATH:
    LOCAL_SETTINGS_PATH = "local/settings.dev.py"

# make LOCAL_SETTINGS_PATH absolute if relative path
if not os.path.isabs(LOCAL_SETTINGS_PATH):
    LOCAL_SETTINGS_PATH = str(BASE_DIR / LOCAL_SETTINGS_PATH)

include(
    "base.py",
    "logging.py",
    "custom.py",
    optional(LOCAL_SETTINGS_PATH),
    "env_vars.py",
    "docker.py",
)
