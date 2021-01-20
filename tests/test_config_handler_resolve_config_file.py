# -*- coding: utf-8 -*-
"""pype.config_handler.resolve_config_file."""

from os import environ, path

import pytest

from pype.config_handler import (DEFAULT_CONFIG, ConfigResolverSource,
                                 PypeConfigHandler)
from pype.constants import ENV_CONFIG_FOLDER
from pype.exceptions import PypeException
from tests import VALID_CONFIG, TestConfigurationType, create_test_env


class TestPypeConfigHandlerResolveConfigFile:  # noqa: D101

    def test_withenv(self) -> None:  # noqa: D102
        with create_test_env(TestConfigurationType.VALID) as test_env:
            environ[ENV_CONFIG_FOLDER] = test_env.config_dir
            config = PypeConfigHandler()
            assert config.get_file_path() == test_env.config_file
            assert config.get_json() == VALID_CONFIG.asdict()
            assert config.get_config_source() == ConfigResolverSource.FROM_ENV

    def test_withenv_but_folder_does_not_exist(self) -> None:  # noqa: D102
        environ[ENV_CONFIG_FOLDER] = '/somewhere/'
        with pytest.raises(PypeException):
            PypeConfigHandler()
        del environ[ENV_CONFIG_FOLDER]

    def test_withdefaultfile(self) -> None:  # noqa: D102
        with create_test_env(TestConfigurationType.VALID) as test_env:
            config = PypeConfigHandler(
                test_env.config_dir, test_env.config_file
            )
            assert config.get_file_path() == test_env.config_file
            assert config.get_json() == VALID_CONFIG.asdict()
            assert config.get_config_source() == (
                ConfigResolverSource.FROM_DEFAULT_PATH)

    def test_onthefly_to_default(self) -> None:  # noqa: D102
        with create_test_env(TestConfigurationType.NONE) as test_env:
            config = PypeConfigHandler(
                test_env.config_dir, 'test_config.json'
            )
            assert config.get_file_path() == path.join(
                test_env.config_dir, 'test_config.json')
            assert config.get_json() == DEFAULT_CONFIG.asdict()
            assert config.get_config_source() == (
                ConfigResolverSource.FROM_SCRATCH_TO_DEFAULT_PATH)

    def test_onthefly_to_provided(self) -> None:  # noqa: D102
        with create_test_env(TestConfigurationType.NONE) as test_env:
            environ[ENV_CONFIG_FOLDER] = test_env.config_dir
            config = PypeConfigHandler()
            assert config.get_file_path() == path.join(
                test_env.config_dir, 'config.json')
            assert config.get_json() == DEFAULT_CONFIG.asdict()
            assert config.get_config_source() == (
                ConfigResolverSource.FROM_SCRATCH_TO_PROVIDED_PATH)
