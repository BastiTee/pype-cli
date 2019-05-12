#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import importlib
import logging
from json import load
from os.path import dirname
import sys
from pype.plugin_type import Plugin
from pype.util.misc import get_or_default


class PypeCore():

    DEFAULT_CONFIG_FILE = 'config.json'
    DEFAULT_LOG_LEVEL = 'INFO'
    DEFAULT_LOG_FORMAT = (
        '%(asctime)-15s %(levelname)s %(message)s [%(name)s.%(funcName)s]'
    )

    def __init__(self, config_file, verbose, list_pypes, pype):
        cfg = self.load_configuration(config_file)
        self.configure_logging(cfg, verbose)
        self.log.debug('Initializing pype: {}'.format(pype))
        self.plugins = [
            Plugin(plugin)
            for plugin in get_or_default(cfg, 'plugins', [])
        ]
        if list_pypes:
            self.print_docu()
        else:
            self.run_pype(self.plugins, pype)

    def run_pype(self, reg, args_pype):
        if not args_pype:
            print('No pype selected.')
            exit(0)
        root_cmd = args_pype[0]
        for plugin in self.plugins:
            for pype in plugin.pypes:
                if not pype.name == root_cmd:
                    continue
                self.log.debug('Invoking script \'{}\''.format(
                    plugin.name + '.' + pype.name))
                # This will trigger any script not supporting main()
                pype = importlib.import_module(plugin.name + '.' + pype.name)
                try:
                    # And this any main() based script
                    sys.args = pype
                    pype.main()
                except AttributeError:
                    pass
                return
        self.log.info('Pype not found: \'{}\''.format(root_cmd))

    def load_configuration(self, cfg_path):
        cfg_path = cfg_path if cfg_path else self.DEFAULT_CONFIG_FILE
        return load(open(cfg_path, 'r'))

    def configure_logging(self, cfg, verbose):
        default_loglevel = (
            'DEBUG' if verbose
            else get_or_default(cfg, 'core.loglevel', self.DEFAULT_LOG_LEVEL))
        logging.basicConfig(
            level=default_loglevel,
            format=get_or_default(cfg,
                                  'core.logformat', self.DEFAULT_LOG_FORMAT)
        )
        self.log = logging.getLogger(__name__)

    def print_docu(self):
        for plugin in self.plugins:
            print('PLUGIN: {} ({})'.format(
                plugin.name.upper(), plugin.doc))
            for pype in plugin.pypes:
                print('\t{} - {}'.format(
                    pype.name, pype.doc
                ))
            print()


def get_pype_basepath():
    return dirname(dirname(__file__))
