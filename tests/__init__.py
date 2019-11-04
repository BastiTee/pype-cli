"""pype-cli test suite."""

import tempfile
from json import dumps
from os import environ
from tempfile import NamedTemporaryFile

from click.testing import CliRunner

from pype.constants import ENV_CONFIG_FILE

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


def invoke_isolated_runner(component_under_test, arguments=[]):
    """Use click.CliRunner to component-test on isolated file system."""
    set_temporary_config_file()
    runner = CliRunner()
    with runner.isolated_filesystem():
        return runner.invoke(component_under_test, arguments), runner


def set_temporary_config_file():
    """Point to a temporary config file."""
    temp_file = tempfile.NamedTemporaryFile()
    environ[ENV_CONFIG_FILE] = temp_file.name


def create_temporary_config_file():
    """Create a temporary configuration file for testing purposes."""
    temp = NamedTemporaryFile()
    temp.write(bytes(dumps(VALID_CONFIG), 'utf-8'))
    temp.seek(0)
    return temp
