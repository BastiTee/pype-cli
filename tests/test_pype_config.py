# -*- coding: utf-8 -*-
"""Pype configuration tests."""

import copy
from json import dumps
from os import environ, remove
from tempfile import NamedTemporaryFile

from pype.pype_config import PypeConfig
from pype.pype_constants import ENV_CONFIG_FILE
from pype.pype_exception import PypeException

from pytest import raises


class TestPypeConfig():
    """Pype configuration tests."""

    # Helpers

    def _create_temporary_config_file(self, json):
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
        'initfile': '~/.pype-initfile'
    }

    # PypeConfig.resolve_config_file()

    def test_resolve_config_file_withenv(self):
        """Config file found via environment variable."""
        tmpf = self._create_temporary_config_file(self.VALID_CONFIG)
        environ[ENV_CONFIG_FILE] = tmpf.name
        pype_config = PypeConfig()
        pype_config.resolve_config_file()
        assert pype_config.get_filepath() == tmpf.name
        assert pype_config.get_json() == self.VALID_CONFIG
        del environ[ENV_CONFIG_FILE]  # cleanup

    def test_resolve_config_file_withdefaultfile(self):
        """Config file found from default file path."""
        tmpf = self._create_temporary_config_file(self.VALID_CONFIG)
        pype_config = PypeConfig()
        pype_config.DEFAULT_CONFIG_FILE = tmpf.name
        pype_config.LOCAL_CONFIG_FILE = '/does/not/exist'
        pype_config.resolve_config_file()
        assert pype_config.get_filepath() == tmpf.name
        assert pype_config.get_json() == self.VALID_CONFIG

    def test_resolve_config_file_withlocalfile(self):
        """Config file found from custom local file."""
        tmpf = self._create_temporary_config_file(self.VALID_CONFIG)
        pype_config = PypeConfig()
        pype_config.DEFAULT_CONFIG_FILE = '/does/not/exist'
        pype_config.LOCAL_CONFIG_FILE = tmpf.name
        pype_config.resolve_config_file()
        assert pype_config.get_filepath() == tmpf.name
        assert pype_config.get_json() == self.VALID_CONFIG

    def test_resolve_config_file_withontheflycreation(self):
        """Config file not found and created on the fly."""
        pype_config = PypeConfig()
        pype_config.DEFAULT_CONFIG_FILE = 'test_config.json'
        pype_config.LOCAL_CONFIG_FILE = '/does/not/exist'
        pype_config.resolve_config_file()
        assert pype_config.get_filepath() == 'test_config.json'
        assert pype_config.get_json() == pype_config.DEFAULT_CONFIG
        remove('test_config.json')  # cleanup

    # PypeConfig.validate_config()

    def test_validate_config_noneInput_raiseTypeError(self):
        """Config validation without input."""
        pype_config = PypeConfig()
        with raises(PypeException):
            pype_config.validate_config(None)

    def test_validate_config_emptyInput_raiseTypeError(self):
        """Config validation with empty input."""
        pype_config = PypeConfig()
        with raises(PypeException):
            pype_config.validate_config({})

    def test_validate_config_validFullJson(self):
        """Config validation with valid JSON."""
        pype_config = PypeConfig()
        assert pype_config.validate_config(self.VALID_CONFIG)

    def test_validate_config_validFullJsonWithExtensions(self):
        """Config validation with valid JSON and more properties."""
        pype_config = PypeConfig()
        input_config = copy.deepcopy(self.VALID_CONFIG)
        input_config['additional_property'] = {}
        assert pype_config.validate_config(input_config)

    def test_validate_config_missingAliasesAttribute(self):
        """Config validation with missing roots."""
        pype_config = PypeConfig()
        input_config = {
            'plugins': []
        }
        with raises(PypeException):
            pype_config.validate_config(input_config)

    def test_validate_config_misconfiguredPlugin(self):
        """Config validation with missing roots."""
        pype_config = PypeConfig()
        input_config = copy.deepcopy(self.VALID_CONFIG)
        input_config['plugins'].append({
            'name': 'new_plugin'
        })
        with raises(PypeException):
            pype_config.validate_config(input_config)

    def test_validate_config_configuredPlugin(self):
        """Config validation with correctly configured additional plugin."""
        pype_config = PypeConfig()
        input_config = copy.deepcopy(self.VALID_CONFIG)
        input_config['plugins'].append({
            'name': 'new_plugin',
            'path': '/some/path',
            'users': []
        })
        assert pype_config.validate_config(input_config)

    def test_validate_config_misconfiguredUserInPlugin(self):
        """Config validation with misconfigured additional plugin."""
        pype_config = PypeConfig()
        input_config = copy.deepcopy(self.VALID_CONFIG)
        input_config['plugins'].append({
            'name': 'new_plugin',
            'path': '/some/path',
            'users': [42]
        })
        with raises(PypeException):
            pype_config.validate_config(input_config)

    def test_validate_config_configuredAlias(self):
        """Config validation with correctly configured additional alias."""
        pype_config = PypeConfig()
        input_config = copy.deepcopy(self.VALID_CONFIG)
        input_config['aliases'].append({
            'alias': 'al',
            'command': 'pype test'
        })
        assert pype_config.validate_config(input_config)

    def test_validate_config_misconfiguredAlias(self):
        """Config validation with misconfigured additional alias."""
        pype_config = PypeConfig()
        input_config = copy.deepcopy(self.VALID_CONFIG)
        input_config['aliases'].append({
            'aliass': 'al',
            'commando': 'pype test'
        })
        with raises(PypeException):
            pype_config.validate_config(input_config)

    def test_validate_config_configuredInitfile(self):
        """Config validation with configured initfile."""
        pype_config = PypeConfig()
        input_config = copy.deepcopy(self.VALID_CONFIG)
        input_config['initfile'] = '/some/path'
        assert pype_config.validate_config(input_config)

    def test_validate_config_misconfiguredInitfile(self):
        """Config validation with misconfigured initfile."""
        pype_config = PypeConfig()
        input_config = copy.deepcopy(self.VALID_CONFIG)
        input_config['initfile'] = {}
        with raises(PypeException):
            pype_config.validate_config(input_config)
