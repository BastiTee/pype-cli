#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import code
import importlib
import inspect
import logging
import os
from json import load
from re import sub

from pype.pype_exception import PypeConfigurationException
from pype.util.iotools import get_immediate_subfiles
from pype.util.misc import get_or_default


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
        self.plugin_registry = {}
        for plugin in get_or_default(cfg, 'pypes', []):
            self.init_plugin(plugin)
        self.log.debug('Loaded plugins:\n{}'.format(
            self.prettify_plugin_registry()))
        self.invoke_matching_pype(self.plugin_registry, args.pype_command)

    def init_plugin(self, plugin):
        # Load remote module via importlib
        try:
            plugin_mod = importlib.import_module(plugin)
        except ModuleNotFoundError as e:
            raise PypeConfigurationException(e)
        # Setup plugin registry
        reg = {'name': plugin, 'module': plugin_mod}
        reg['abspath'] = os.path.dirname(inspect.getabsfile(plugin_mod))
        reg['cmds'] = self.resolve_pypes(reg['abspath'], plugin)
        reg['doc'] = self.get_docu_or_default(plugin_mod)
        # Register
        self.plugin_registry[plugin] = reg

    def resolve_pypes(self, abspath, plugin_name):
        cmds = get_immediate_subfiles(abspath, r'^(?!__).*(?!__)\.py$')
        pypes = []
        for cmd in cmds:
            abspath_cmd = os.path.join(abspath, cmd)
            pype = {
                'name': sub(r'\.py$', '', cmd),
                'doc': self.get_module_docstring(abspath_cmd)
            }
            pypes.append(pype)
        return pypes

    def get_module_docstring(self, filepath):
        """Get module-level docstring of Python module at filepath."""
        co = compile(open(filepath).read(), filepath, 'exec')
        if co.co_consts and isinstance(co.co_consts[0], str):
            return sub(r'[\.]+$', '', co.co_consts[0])
        return 'Not documented yet'

    def get_docu_or_default(self, module):
        return (
            sub(r'[\.]+$', '', module.__doc__)  # replace trailing dots
            if module.__doc__ else 'Not documented yet'
        )

    def invoke_matching_pype(self, reg, pype):
        if not pype:
            print('No pype selected.')
            exit(0)
        root_cmd = pype[0]
        for key in reg.keys():
            mod = reg[key]
            for cmd in mod['cmds']:
                if not cmd['name'] == root_cmd:
                    continue
                importlib.import_module(mod['name'] + '.' + cmd['name'])
                return
        self.log.info('No matching pype for name \'{}\'.'.format(pype))

    def load_configuration(self, cfg_path):
        cfg_path = cfg_path if cfg_path else self.DEFAULT_CONFIG_FILE
        return load(open(cfg_path, 'r'))

    def prettify_plugin_registry(self):
        plugin_docu = []
        for plugin in self.plugin_registry:
            pg = self.plugin_registry.get(plugin)
            plugin_docu.append(plugin.upper())
            for key in pg.keys():
                plugin_docu.append(' - {} = {}'.format(key, pg[key]))
        return '\n'.join(plugin_docu)
