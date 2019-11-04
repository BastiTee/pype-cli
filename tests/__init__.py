"""pype-cli test suite."""

from collections import namedtuple
from json import dump, load
from os import environ

from click.testing import CliRunner

from pype import resolve_path
from pype.config_handler import DEFAULT_CONFIG
from pype.constants import ENV_TEST_CONFIG_FILE

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


RunnerModel = namedtuple(
    'RunnerModel',
    'result runner config_file'
)


def invoke_isolated_test(component_under_test, arguments=[]):
    """Use click.CliRunner to component-test on isolated file system."""
    temp_file = create_temporary_config_file(DEFAULT_CONFIG)
    environ[ENV_TEST_CONFIG_FILE] = temp_file
    runner = CliRunner(env=environ)
    with runner.isolated_filesystem():
        if component_under_test == 'main':
            from pype import __main__
            component_under_test = __main__.main
        return RunnerModel(
            result=runner.invoke(component_under_test, arguments, env=environ),
            runner=runner,
            config_file=temp_file)


def load_config_from_test(test_run):
    """Load configuration of test as JSON-object."""
    print('- read temporary from {}'.format(test_run.config_file))
    return load(open(test_run.config_file, 'r'))


def create_temporary_config_file(configuration=VALID_CONFIG):
    """Create a temporary configuration file for testing purposes."""
    temp_file = resolve_path('~/.pype-test-configuration.json')
    dump(configuration, open(temp_file, 'w+'))
    print('- created temporary test config at {}'.format(temp_file))
    return temp_file
