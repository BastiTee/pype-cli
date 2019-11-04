"""pype-cli test suite."""

import tempfile
from os import environ

from pype.constants import ENV_CONFIG_FILE
from json import dumps
from tempfile import NamedTemporaryFile

VALID_CONFIG = {
    'plugins': [
        {
            'name': 'plugin_name',
            'path': '~/some/path',
            'users': ['someuser']
        }
    ],
    'aliases': [
        {
            'alias': 'alias_name',
            'command': 'pype myplugin mypype'
        }
    ],
    'core_config': {
    }
}


def set_temporary_config_file():
    """Point to a temporary config file."""
    temp_file = tempfile.NamedTemporaryFile()
    environ[ENV_CONFIG_FILE] = temp_file.name


def create_temporary_config_file():
    temp = NamedTemporaryFile()
    temp.write(bytes(dumps(VALID_CONFIG), 'utf-8'))
    temp.seek(0)
    return temp
