#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import importlib
import logging
from json import load

from plugin_type import Plugin
from util.misc import get_or_default


class PypeCore():

    DEFAULT_CONFIG_FILE = 'config.json'
    DEFAULT_LOG_LEVEL = 'INFO'
    DEFAULT_LOG_FORMAT = (
        '%(asctime)-15s %(levelname)s %(message)s [%(name)s.%(funcName)s]'
    )

    def __init__(self, args):
        cfg = self.load_configuration(args.c)
        default_loglevel = (
            'DEBUG' if args.v
            else get_or_default(cfg, 'core.loglevel', self.DEFAULT_LOG_LEVEL))
        logging.basicConfig(
            level=default_loglevel,
            format=get_or_default(cfg,
                                  'core.logformat', self.DEFAULT_LOG_FORMAT)
        )
        self.log = logging.getLogger(__name__)
        self.log.debug('Initializing pype...')
        self.plugin_pypes = [
            Plugin(plugin)
            for plugin in get_or_default(cfg, 'plugin_pypes', [])
        ]
        self.log.debug('Loaded plugins:\n{}'.format(
            self.prettify_plugin_registry()))
        self.invoke_matching_pype(self.plugin_pypes, args.pype_command)

    def invoke_matching_pype(self, reg, cmdline):
        if not cmdline:
            print('No pype selected.')
            exit(0)
        root_cmd = cmdline[0]
        for plugin in self.plugin_pypes:
            for pype in plugin.pypes:
                if not pype.name == root_cmd:
                    continue
                importlib.import_module(plugin.name + '.' + pype.name)
                return
        self.log.info('No matching pype for name \'{}\'.'.format(root_cmd))

    def load_configuration(self, cfg_path):
        cfg_path = cfg_path if cfg_path else self.DEFAULT_CONFIG_FILE
        return load(open(cfg_path, 'r'))

    def prettify_plugin_registry(self):
        plugin_docu = []
        for plugin in self.plugin_pypes:
            plugin_docu.append(plugin.name.upper())
            for pype in plugin.pypes:
                plugin_docu.append(' - {} = {}'.format(pype.name, pype.docu))
        return '\n'.join(plugin_docu)
