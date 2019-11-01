"""pype-cli test suite."""

import tempfile
from os import environ

from pype.constants import ENV_CONFIG_FILE


def set_temporary_config_file():
    """Point to a temporary config file."""
    temp_file = tempfile.NamedTemporaryFile()
    environ[ENV_CONFIG_FILE] = temp_file.name
