"""pype-cli test suite."""

import contextlib
import importlib
import shutil
from collections import namedtuple
from enum import Enum
from json import dump, load
from os import chdir, environ, mkdir, path
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
    'working_dir config_file'
)


class Configuration(Enum):
    """Configuration selection."""

    EMPTY = 0
    VALID = 1


@contextlib.contextmanager
def create_test_env(configuration=Configuration.EMPTY):
    """Create a temporary configuration file for testing purposes."""
    test_base_folder = resolve_path('~/.pype-cli-tests')
    if not path.isdir(test_base_folder):
        mkdir(test_base_folder)
    working_dir = path.join(
        test_base_folder,
        ''.join(choice(ascii_lowercase) for i in range(20)))
    mkdir(working_dir)
    chdir(working_dir)
    config_file = path.join(working_dir, 'config.json')
    config = (
        DEFAULT_CONFIG
        if configuration == Configuration.EMPTY else VALID_CONFIG
    )
    dump(config, open(config_file, 'w+'))
    try:
        yield TestEnvironment(
            working_dir=working_dir,
            config_file=config_file
        )
    finally:
        shutil.rmtree(working_dir)


def invoke_runner(component_under_test, arguments=[]):
    """Create and invoke a test runner."""
    with create_test_env() as test_env:
        return create_runner(test_env, component_under_test, arguments)


def create_runner(test_env, component_under_test, arguments=[]):
    """Create a test runner with a provided test environment.

    We need to delay the import of pype.__main__ until we set the environment
    variables correctly. That is why tests.invoke_runner gets called
    with a string instead of a module.
    """
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
