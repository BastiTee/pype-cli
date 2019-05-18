#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import logging
from json import load
from pype.plugin_type import Plugin
from pype.util.misc import get_or_default


class PypeCore():

    DEFAULT_CONFIG_FILE = 'config.json'
    DEFAULT_LOG_LEVEL = 'INFO'
    DEFAULT_LOG_FORMAT = (
        '%(asctime)-15s %(levelname)s %(message)s [%(name)s.%(funcName)s]'
    )

    def __init__(self, config_file):
        self.cfg = self.load_configuration(config_file)
        self.plugins = [
            Plugin(plugin)
            for plugin in get_or_default(self.cfg, 'plugins', [])
        ]

    def get_plugins(self):
        return self.plugins

    def load_configuration(self, cfg_path):
        cfg_path = cfg_path if cfg_path else self.DEFAULT_CONFIG_FILE
        return load(open(cfg_path, 'r'))

    def configure_logging(self, verbose):
        default_loglevel = (
            'DEBUG' if verbose
            else get_or_default(
                self.cfg, 'core.loglevel', self.DEFAULT_LOG_LEVEL))
        logging.basicConfig(
            level=default_loglevel,
            format=get_or_default(
                self.cfg, 'core.logformat', self.DEFAULT_LOG_FORMAT)
        )
        self.log = logging.getLogger(__name__)
        self.log.debug('Debugging activated.')

    def list_pypes(self):
        for plugin in self.plugins:
            print('PLUGIN: {} ({}) @ {}'.format(
                plugin.name.upper(), plugin.doc, plugin.abspath))
            for pype in plugin.pypes:
                print('\t{} - {}\n\t@ {}'.format(
                    pype.name, pype.doc, pype.abspath
                ))
            print()
