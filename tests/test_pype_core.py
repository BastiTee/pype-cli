# -*- coding: utf-8 -*-

from pype.pype_core import PypeCore
from os import environ, remove
from tempfile import NamedTemporaryFile
from json import dumps


class TestPypeCore:

    def create_temporary_config_file(self, json):
        temp = NamedTemporaryFile()
        if json:
            temp.write(bytes(dumps(json), 'utf-8'))
        temp.seek(0)
        return temp

    def test_resolve_config_file_withenv(self):
        tmpf = self.create_temporary_config_file({'key': 'env'})
        environ['PYPE_CONFIG_JSON'] = tmpf.name
        pype_core = PypeCore()
        pype_core.resolve_config_file()
        assert pype_core.get_config_filepath() == tmpf.name
        assert pype_core.get_config_json() == {'key': 'env'}
        del environ['PYPE_CONFIG_JSON']  # cleanup

    def test_resolve_config_file_withdefaultfile(self):
        tmpf = self.create_temporary_config_file({'key': 'default'})
        pype_core = PypeCore()
        pype_core.DEFAULT_CONFIG_FILE = tmpf.name
        pype_core.LOCAL_CONFIG_FILE = '/does/not/exist'
        pype_core.resolve_config_file()
        assert pype_core.get_config_filepath() == tmpf.name
        assert pype_core.get_config_json() == {'key': 'default'}

    def test_resolve_config_file_withlocalfile(self):
        tmpf = self.create_temporary_config_file({'key': 'local'})
        pype_core = PypeCore()
        pype_core.DEFAULT_CONFIG_FILE = '/does/not/exist'
        pype_core.LOCAL_CONFIG_FILE = tmpf.name
        pype_core.resolve_config_file()
        assert pype_core.get_config_filepath() == tmpf.name
        assert pype_core.get_config_json() == {'key': 'local'}

    def test_resolve_config_file_withontheflycreation(self):
        pype_core = PypeCore()
        pype_core.DEFAULT_CONFIG_FILE = 'test_config.json'
        pype_core.LOCAL_CONFIG_FILE = '/does/not/exist'
        pype_core.resolve_config_file()
        assert pype_core.get_config_filepath() == 'test_config.json'
        assert pype_core.get_config_json() == pype_core.DEFAULT_CONFIG
        remove('test_config.json')  # cleanup
