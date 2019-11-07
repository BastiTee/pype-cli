# -*- coding: utf-8 -*-
"""pype.config_handler.resolve_config_file."""

from os import environ, path

from pype.config_handler import (
    ConfigResolverSource, DEFAULT_CONFIG, PypeConfigHandler)
from pype.constants import ENV_CONFIG_FOLDER
from pype.exceptions import PypeException

import pytest

from tests import Configuration, VALID_CONFIG, create_test_env


class TestPypeConfigHandlerResolveConfigFile:  # noqa: D101

    @pytest.fixture(autouse=True)
    def _run_around_tests(self):
        # Before each
        try:
            del environ[ENV_CONFIG_FOLDER]
        except KeyError:
            pass

    def test_withenv(self):  # noqa: D102
        with create_test_env(Configuration.VALID) as test_env:
            environ[ENV_CONFIG_FOLDER] = test_env.config_dir
            config = PypeConfigHandler(init=False)
            source = config.resolve_config_file()
            assert config.get_filepath() == test_env.config_file
            assert config.get_json() == VALID_CONFIG
            assert source == ConfigResolverSource.FROM_ENV

    def test_withenv_but_folder_does_not_exist(self):  # noqa: D102
        environ[ENV_CONFIG_FOLDER] = '/somewhere/'
        config = PypeConfigHandler(init=False)
        with pytest.raises(PypeException):
            config.resolve_config_file()

    def test_withdefaultfile(self):  # noqa: D102
        with create_test_env(Configuration.VALID) as test_env:
            config = PypeConfigHandler(init=False)
            config.DEFAULT_CONFIG_FILE = test_env.config_file
            config.LOCAL_CONFIG_FILE = '/does/not/exist'
            source = config.resolve_config_file()
            assert config.get_filepath() == test_env.config_file
            assert config.get_json() == VALID_CONFIG
            assert source == ConfigResolverSource.FROM_DEFAULT_PATH

    def test_onthefly_to_default(self):  # noqa: D102
        with create_test_env(Configuration.NONE) as test_env:
            config = PypeConfigHandler(init=False)
            config.DEFAULT_CONFIG_FOLDER = test_env.config_dir
            config.DEFAULT_CONFIG_FILE = 'test_config.json'
            config.LOCAL_CONFIG_FILE = '/does/not/exist'
            source = config.resolve_config_file()
            assert config.get_filepath() == path.join(
                test_env.config_dir, 'test_config.json')
            assert config.get_json() == DEFAULT_CONFIG
            assert source == ConfigResolverSource.FROM_SCRATCH_TO_DEFAULT_PATH

    def test_onthefly_to_provided(self):  # noqa: D102
        with create_test_env(Configuration.NONE) as test_env:
            environ[ENV_CONFIG_FOLDER] = test_env.config_dir
            config = PypeConfigHandler(init=False)
            source = config.resolve_config_file()
            assert config.get_filepath() == path.join(
                test_env.config_dir, 'config.json')
            assert config.get_json() == DEFAULT_CONFIG
            assert source == ConfigResolverSource.FROM_SCRATCH_TO_PROVIDED_PATH
