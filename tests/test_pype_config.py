# -*- coding: utf-8 -*-
"""Pype configuration tests."""

import copy
from json import dumps
from os import environ, path, remove
from tempfile import NamedTemporaryFile

from pype.config_handler import PypeConfigHandler
from pype.constants import ENV_CONFIG_FILE
from pype.exceptions import PypeException

from pytest import raises


class TestPypeConfigHandler:
    """Pype configuration tests."""

    @staticmethod
    def _create_temporary_config_file(json):
        temp = NamedTemporaryFile()
        if json:
            temp.write(bytes(dumps(json), 'utf-8'))
        temp.seek(0)
        return temp

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

    def test_resolve_config_file_withenv(self):
        """Config file found via environment variable."""
        tmpf = self._create_temporary_config_file(self.VALID_CONFIG)
        environ[ENV_CONFIG_FILE] = tmpf.name
        config = PypeConfigHandler()
        config.resolve_config_file()
        assert config.get_filepath() == tmpf.name
        assert config.get_json() == self.VALID_CONFIG
        del environ[ENV_CONFIG_FILE]  # cleanup

    def test_resolve_config_file_withdefaultfile(self):
        """Config file found from default file path."""
        tmpf = self._create_temporary_config_file(self.VALID_CONFIG)
        config = PypeConfigHandler()
        config.DEFAULT_CONFIG_FILE = tmpf.name
        config.LOCAL_CONFIG_FILE = '/does/not/exist'
        config.resolve_config_file()
        assert config.get_filepath() == tmpf.name
        assert config.get_json() == self.VALID_CONFIG

    def test_resolve_config_file_withlocalfile(self):
        """Config file found from custom local file."""
        tmpf = self._create_temporary_config_file(self.VALID_CONFIG)
        config = PypeConfigHandler()
        config.DEFAULT_CONFIG_FILE = '/does/not/exist'
        config.LOCAL_CONFIG_FILE = tmpf.name
        config.resolve_config_file()
        assert config.get_filepath() == tmpf.name
        assert config.get_json() == self.VALID_CONFIG

    def test_resolve_config_file_withontheflycreation(self):
        """Config file not found and created on the fly."""
        config = PypeConfigHandler()
        if path.isfile('test_config.json'):
            remove('test_config.json')
        config.DEFAULT_CONFIG_FILE = 'test_config.json'
        config.LOCAL_CONFIG_FILE = '/does/not/exist'
        config.resolve_config_file()
        assert config.get_filepath() == 'test_config.json'
        assert config.get_json() == config.DEFAULT_CONFIG
        remove('test_config.json')  # cleanup

    # PypeConfigHandler.validate_config()

    def test_validate_config_noneinput_raisetypeerror(self):
        """Config validation without input."""
        config = PypeConfigHandler()
        with raises(PypeException):
            config.validate_config(None)

    def test_validate_config_emptyinput_raisetypeerror(self):
        """Config validation with empty input."""
        config = PypeConfigHandler()
        with raises(PypeException):
            config.validate_config({})

    def test_validate_config_validfulljson(self):
        """Config validation with valid JSON."""
        config = PypeConfigHandler()
        assert config.validate_config(self.VALID_CONFIG)

    def test_validate_config_validfulljsonwithextensions(self):
        """Config validation with valid JSON and more properties."""
        config = PypeConfigHandler()
        input_config = copy.deepcopy(self.VALID_CONFIG)
        input_config['additional_property'] = {}
        assert config.validate_config(input_config)

    def test_validate_config_missingaliasesattribute(self):
        """Config validation with missing roots."""
        config = PypeConfigHandler()
        input_config = {
            'plugins': []
        }
        with raises(PypeException):
            config.validate_config(input_config)

    def test_validate_config_misconfiguredplugin(self):
        """Config validation with missing roots."""
        config = PypeConfigHandler()
        input_config = copy.deepcopy(self.VALID_CONFIG)
        input_config['plugins'].append({
            'name': 'new_plugin'
        })
        with raises(PypeException):
            config.validate_config(input_config)

    def test_validate_config_configuredplugin(self):
        """Config validation with correctly configured additional plugin."""
        config = PypeConfigHandler()
        input_config = copy.deepcopy(self.VALID_CONFIG)
        input_config['plugins'].append({
            'name': 'new_plugin',
            'path': '/some/path',
            'users': []
        })
        assert config.validate_config(input_config)

    def test_validate_config_misconfigureduserinplugin(self):
        """Config validation with misconfigured additional plugin."""
        config = PypeConfigHandler()
        input_config = copy.deepcopy(self.VALID_CONFIG)
        input_config['plugins'].append({
            'name': 'new_plugin',
            'path': '/some/path',
            'users': [42]
        })
        with raises(PypeException):
            config.validate_config(input_config)

    def test_validate_config_configuredalias(self):
        """Config validation with correctly configured additional alias."""
        config = PypeConfigHandler()
        input_config = copy.deepcopy(self.VALID_CONFIG)
        input_config['aliases'].append({
            'alias': 'al',
            'command': 'pype test'
        })
        assert config.validate_config(input_config)

    def test_validate_config_misconfiguredalias(self):
        """Config validation with misconfigured additional alias."""
        config = PypeConfigHandler()
        input_config = copy.deepcopy(self.VALID_CONFIG)
        input_config['aliases'].append({
            'aliass': 'al',
            'commando': 'pype test'
        })
        with raises(PypeException):
            config.validate_config(input_config)
