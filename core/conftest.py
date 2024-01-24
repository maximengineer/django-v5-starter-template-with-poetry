import os

os.environ["PYTEST_RUNNING"] = "true"

from core.general.tests.fixtures import *  # noqa: F401, F403, E402
