# -*- coding: utf-8 -*-

from pype.pype_config import PypeConfig
from os import environ, remove
from tempfile import NamedTemporaryFile
from json import dumps


class TestPypeConfig:

    def create_temporary_config_file(self, json):
        temp = NamedTemporaryFile()
        if json:
            temp.write(bytes(dumps(json), 'utf-8'))
        temp.seek(0)
        return temp

    def test_resolve_config_file_withenv(self):
        tmpf = self.create_temporary_config_file({'key': 'env'})
        environ['PYPE_CONFIGURATION_FILE'] = tmpf.name
        pype_config = PypeConfig()
        pype_config.resolve_config_file()
        assert pype_config.get_filepath() == tmpf.name
        assert pype_config.get_json() == {'key': 'env'}
        del environ['PYPE_CONFIGURATION_FILE']  # cleanup

    def test_resolve_config_file_withdefaultfile(self):
        tmpf = self.create_temporary_config_file({'key': 'default'})
        pype_config = PypeConfig()
        pype_config.DEFAULT_CONFIG_FILE = tmpf.name
        pype_config.LOCAL_CONFIG_FILE = '/does/not/exist'
        pype_config.resolve_config_file()
        assert pype_config.get_filepath() == tmpf.name
        assert pype_config.get_json() == {'key': 'default'}

    def test_resolve_config_file_withlocalfile(self):
        tmpf = self.create_temporary_config_file({'key': 'local'})
        pype_config = PypeConfig()
        pype_config.DEFAULT_CONFIG_FILE = '/does/not/exist'
        pype_config.LOCAL_CONFIG_FILE = tmpf.name
        pype_config.resolve_config_file()
        assert pype_config.get_filepath() == tmpf.name
        assert pype_config.get_json() == {'key': 'local'}

    def test_resolve_config_file_withontheflycreation(self):
        pype_config = PypeConfig()
        pype_config.DEFAULT_CONFIG_FILE = 'test_config.json'
        pype_config.LOCAL_CONFIG_FILE = '/does/not/exist'
        pype_config.resolve_config_file()
        assert pype_config.get_filepath() == 'test_config.json'
        assert pype_config.get_json() == pype_config.DEFAULT_CONFIG
        remove('test_config.json')  # cleanup
