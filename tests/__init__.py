# -*- coding: utf-8 -*-
"""pype-cli test suite."""

import contextlib
import importlib
import shutil
from collections import namedtuple
from dataclasses import asdict
from datetime import datetime
from enum import Enum
from json import dump, load
from os import environ, mkdir, path
from random import choice
from re import sub
from string import ascii_lowercase
from typing import Generator, Optional, Union, cast

from click.core import BaseCommand
from click.testing import CliRunner

from pype import __main__, config_model, resolve_path
from pype.config_handler import DEFAULT_CONFIG
from pype.constants import ENV_CONFIG_FOLDER
from pype.core import in_virtualenv

VALID_CONFIG = config_model.Configuration(
    core_config=config_model.ConfigurationCore(),
    plugins=[config_model.ConfigurationPlugin(
        name='plugin_name', path='~/some/path', users=['someuser']
    )],
    aliases=[config_model.ConfigurationAlias(
        alias='alias_name', command='pype myplugin mypype'
    )]
)

RunnerEnvironment = namedtuple(
    'RunnerEnvironment',
    'result runner reload_and_get_main test_env'
)

TestEnvironment = namedtuple(
    'TestEnvironment',
    'config_dir config_file'
)


class ConfigTypeForTest(Enum):
    """Type of configuration selection."""

    EMPTY = 0
    VALID = 1
    NONE = 2


@ contextlib.contextmanager
def create_test_env(
    configuration: ConfigTypeForTest = ConfigTypeForTest.EMPTY
) -> Generator[
        TestEnvironment, None, None]:
    """Create a temporary configuration folder for testing purposes."""
    # Setup base folder
    test_base_folder = resolve_path('./.venv/pype-cli-tests')
    activate_file = resolve_path('./.venv/bin/activate')
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
    config: Optional[config_model.Configuration] = None
    if configuration == ConfigTypeForTest.EMPTY:
        config = DEFAULT_CONFIG
    elif configuration == ConfigTypeForTest.VALID:
        config = VALID_CONFIG
    elif configuration == ConfigTypeForTest.NONE:
        config = None
    if config:
        dump(asdict(config), open(config_file, 'w+'))
    # Yield
    try:
        yield TestEnvironment(
            config_dir=config_dir,
            config_file=config_file
        )
    finally:
        shutil.rmtree(test_base_folder)
        # cleanup shell rc
        if in_virtualenv():
            activate_file_h = open(activate_file, 'r')
            activate_lines = activate_file_h.readlines()
            activate_file_h.close()
            # activate_file_h = open(activate_file, 'w')
            activate_lines = [
                line for line in activate_lines if '# pype-cli' not in line
            ]
            activate_file_h = open(activate_file, 'w')
            [activate_file_h.write(line) for line in activate_lines]
            activate_file_h.close()
        try:
            del environ[ENV_CONFIG_FOLDER]
        except KeyError:
            pass  # Might not have been set but if so it has to be deleted


def invoke_runner(
        component_under_test: Union[str, BaseCommand],
        arguments: list = None
) -> RunnerEnvironment:
    """Create and invoke a test runner."""
    if arguments is None:
        arguments = []
    with create_test_env() as test_env:
        return create_runner(test_env, component_under_test, arguments)


def create_runner(
        test_env: TestEnvironment,
        component_under_test: Union[str, BaseCommand],
        arguments: list = None
) -> RunnerEnvironment:
    """Create a test runner with a provided test environment.

    We need to delay the import of pype.__main__ until we set the environment
    variables correctly. That is why tests.invoke_runner gets called
    with a string instead of a module.
    """
    if arguments is None:
        arguments = []
    environ[ENV_CONFIG_FOLDER] = test_env.config_dir
    runner = CliRunner(env=environ)
    importlib.reload(__main__)
    cot: BaseCommand
    if (
        isinstance(component_under_test, str)
        and component_under_test == r'%MAIN%'
    ):
        cot = __main__.main
    else:
        cot = cast(BaseCommand, component_under_test)
    # Replace %CONFIG_DIR% in arguments with actual test-config dir
    arguments = [
        sub(r'%CONFIG_DIR%', test_env.config_dir, arg) for arg in arguments]
    return RunnerEnvironment(
        result=runner.invoke(cot, arguments, env=environ),
        runner=runner,
        reload_and_get_main=cast(
            BaseCommand, importlib.reload(__main__)
        ).main,
        test_env=test_env
    )


def reload_config(test_run: RunnerEnvironment) -> dict:
    """Load configuration of test as JSON-object."""
    return load(open(test_run.test_env.config_file, 'r'))
