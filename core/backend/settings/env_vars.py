"""
The module takes env variables with a matching prefix, strips out the prefix,
and adds them to dictionary of gloval variables
"""

from core.backend.settings import ENV_VAR_SETTINGS_PREFIX
from core.general.utils.collections import update_dict_with_dict
from core.general.utils.settings import get_settings_from_env

update_dict_with_dict(globals(), get_settings_from_env(ENV_VAR_SETTINGS_PREFIX))
