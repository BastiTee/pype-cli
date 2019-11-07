"""pype-cli test suite."""

import contextlib
import importlib
import shutil
from collections import namedtuple
from datetime import datetime
from enum import Enum
from json import dump, load
from os import environ, mkdir, path
from random import choice
from string import ascii_lowercase

from click.testing import CliRunner

from pype import __main__
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

TestRunner = namedtuple(
    'TestRunner',
    'result runner main test_env'
)

TestEnvironment = namedtuple(
    'TestEnvironment',
    'config_dir config_file'
)


class Configuration(Enum):
    """Configuration selection."""

    EMPTY = 0
    VALID = 1
    NONE = 2


@contextlib.contextmanager
def create_test_env(configuration=Configuration.EMPTY):
    """Create a temporary configuration folder for testing purposes."""
    # Setup base folder
    test_base_folder = resolve_path('./.pype-cli-tests')
    if not path.isdir(test_base_folder):
        mkdir(test_base_folder)
    # Create test environment
    config_dir = path.join(
        test_base_folder,
        datetime.now().strftime('%Y%m%d_%H%M%S') + '_'
        + ''.join(choice(ascii_lowercase) for i in range(20)))
    mkdir(config_dir)
    # Create configuration file
    config_file = path.join(config_dir, 'config.json')
    if configuration == Configuration.EMPTY:
        config = DEFAULT_CONFIG
    elif configuration == Configuration.VALID:
        config = VALID_CONFIG
    elif configuration == Configuration.NONE:
        config = None
    if config:
        dump(config, open(config_file, 'w+'))
    # Yield
    try:
        yield TestEnvironment(
            config_dir=config_dir,
            config_file=config_file
        )
    finally:
        shutil.rmtree(config_dir)


def invoke_runner(component_under_test, arguments=None):
    """Create and invoke a test runner."""
    if arguments is None:
        arguments = []
    with create_test_env() as test_env:
        return create_runner(test_env, component_under_test, arguments)


def create_runner(test_env, component_under_test, arguments=None):
    """Create a test runner with a provided test environment.

    We need to delay the import of pype.__main__ until we set the environment
    variables correctly. That is why tests.invoke_runner gets called
    with a string instead of a module.
    """
    if arguments is None:
        arguments = []
    environ[ENV_TEST_CONFIG_FILE] = test_env.config_file
    runner = CliRunner(env=environ)
    main_lib = importlib.reload(__main__)
    if component_under_test == 'main':
        component_under_test = main_lib.main
    return TestRunner(
        result=runner.invoke(component_under_test, arguments, env=environ),
        runner=runner,
        main=importlib.reload(__main__).main,
        test_env=test_env
    )


def reload_config(test_run):
    """Load configuration of test as JSON-object."""
    return load(open(test_run.test_env.config_file, 'r'))
