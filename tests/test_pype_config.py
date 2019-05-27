# -*- coding: utf-8 -*-
"""Pype configuration tests."""

from json import dumps
from os import environ, remove
from tempfile import NamedTemporaryFile

from pype.pype_config import PypeConfig


class TestPypeConfig:
    """Pype configuration tests."""

    def _create_temporary_config_file(self, json):
        temp = NamedTemporaryFile()
        if json:
            temp.write(bytes(dumps(json), 'utf-8'))
        temp.seek(0)
        return temp

    def test_resolve_config_file_withenv(self):
        """Config file found via environment variable."""
        tmpf = self._create_temporary_config_file({'key': 'env'})
        environ['PYPE_CONFIGURATION_FILE'] = tmpf.name
        pype_config = PypeConfig()
        pype_config.resolve_config_file()
        assert pype_config.get_filepath() == tmpf.name
        assert pype_config.get_json() == {'key': 'env'}
        del environ['PYPE_CONFIGURATION_FILE']  # cleanup

    def test_resolve_config_file_withdefaultfile(self):
        """Config file found from default file path."""
        tmpf = self._create_temporary_config_file({'key': 'default'})
        pype_config = PypeConfig()
        pype_config.DEFAULT_CONFIG_FILE = tmpf.name
        pype_config.LOCAL_CONFIG_FILE = '/does/not/exist'
        pype_config.resolve_config_file()
        assert pype_config.get_filepath() == tmpf.name
        assert pype_config.get_json() == {'key': 'default'}

    def test_resolve_config_file_withlocalfile(self):
        """Config file found from custom local file."""
        tmpf = self._create_temporary_config_file({'key': 'local'})
        pype_config = PypeConfig()
        pype_config.DEFAULT_CONFIG_FILE = '/does/not/exist'
        pype_config.LOCAL_CONFIG_FILE = tmpf.name
        pype_config.resolve_config_file()
        assert pype_config.get_filepath() == tmpf.name
        assert pype_config.get_json() == {'key': 'local'}

    def test_resolve_config_file_withontheflycreation(self):
        """Config file not found and created on the fly."""
        pype_config = PypeConfig()
        pype_config.DEFAULT_CONFIG_FILE = 'test_config.json'
        pype_config.LOCAL_CONFIG_FILE = '/does/not/exist'
        pype_config.resolve_config_file()
        assert pype_config.get_filepath() == 'test_config.json'
        assert pype_config.get_json() == pype_config.DEFAULT_CONFIG
        remove('test_config.json')  # cleanup
