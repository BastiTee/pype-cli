# -*- coding: utf-8 -*-
"""pype.config_handler.resolve_config_file."""

from os import environ, path, remove

from pype.config_handler import ConfigResolverSource, PypeConfigHandler
from pype.constants import ENV_CONFIG_FILE

from pytest import fixture

from tests import VALID_CONFIG, create_temporary_config_file


class TestPypeConfigHandlerResolveConfigFile:  # noqa: D101

    @fixture(autouse=True)
    def _run_around_tests(self):
        # Before each
        try:
            del environ[ENV_CONFIG_FILE]
        except KeyError:
            pass
        # Run test
        yield
        # After each
        if path.isfile('test_config.json'):
            remove('test_config.json')

    def test_withenv(self):  # noqa: D102
        tmpf = create_temporary_config_file()
        environ[ENV_CONFIG_FILE] = tmpf.name
        config = PypeConfigHandler()
        source = config.resolve_config_file()
        assert config.get_filepath() == tmpf.name
        assert config.get_json() == VALID_CONFIG
        assert source == ConfigResolverSource.FROM_ENV

    def test_withdefaultfile(self):  # noqa: D102
        tmpf = create_temporary_config_file()
        config = PypeConfigHandler()
        config.DEFAULT_CONFIG_FILE = tmpf.name
        config.LOCAL_CONFIG_FILE = '/does/not/exist'
        source = config.resolve_config_file()
        assert config.get_filepath() == tmpf.name
        assert config.get_json() == VALID_CONFIG
        assert source == ConfigResolverSource.FROM_DEFAULT_PATH

    def test_withlocalfile(self):  # noqa: D102
        tmpf = create_temporary_config_file()
        config = PypeConfigHandler()
        config.DEFAULT_CONFIG_FILE = '/does/not/exist'
        config.LOCAL_CONFIG_FILE = tmpf.name
        source = config.resolve_config_file()
        assert config.get_filepath() == tmpf.name
        assert config.get_json() == VALID_CONFIG
        assert source == ConfigResolverSource.FROM_RELATIVE_FILE

    def test_withontheflycreation(self):  # noqa: D102
        config = PypeConfigHandler()
        config.DEFAULT_CONFIG_FILE = 'test_config.json'
        config.LOCAL_CONFIG_FILE = '/does/not/exist'
        source = config.resolve_config_file()
        assert config.get_filepath() == 'test_config.json'
        assert config.get_json() == config.DEFAULT_CONFIG
        assert source == ConfigResolverSource.FROM_SCRATCH_TO_DEFAULT_PATH
