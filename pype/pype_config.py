# -*- coding: utf-8 -*-

from json import dump, load
from os import environ
from os.path import dirname, isfile, join

from pype.util.iotools import resolve_path


class PypeConfig():
    """Pype configuration handler."""

    DEFAULT_CONFIG_FILE = resolve_path('~/.pype-config.json')
    LOCAL_CONFIG_FILE = join(dirname(dirname(__file__)), 'config.json')
    DEFAULT_CONFIG = {
        'plugins': [],
        'aliases': []
    }

    def __init__(self):
        self.config = None
        self.filepath = None

    def resolve_config_file(self):
        try:
            # Priority 1: Environment variable
            self.filepath = environ['PYPE_CONFIGURATION_FILE']
        except KeyError:
            # Priority 2: ~/.pype-config.json
            if isfile(self.DEFAULT_CONFIG_FILE):
                self.filepath = self.DEFAULT_CONFIG_FILE
            # Priority 3: ./config.json
            elif isfile(self.LOCAL_CONFIG_FILE):
                self.filepath = self.LOCAL_CONFIG_FILE
        # Priority 4: Create a template config from scratch
        if not self.filepath:
            dump(self.DEFAULT_CONFIG, open(self.DEFAULT_CONFIG_FILE, 'w+'))
            self.filepath = self.DEFAULT_CONFIG_FILE
        self.config = load(open(self.filepath, 'r'))

    def get_json(self):
        if not self.config:
            self.resolve_config_file()
        return self.config

    def get_filepath(self):
        if not self.config:
            self.resolve_config_file()
        return self.filepath

    def set_json(self, config):
        self.config = config
        # always update config file as well
        dump(self.config, open(self.filepath, 'w+'), indent=4)
