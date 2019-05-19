# -*- coding: utf-8 -*-

import importlib
from os import path
from re import sub
from sys import path as syspath

from pype.pype_exception import PypeException
from pype.pype_type import Pype
from pype.util.iotools import get_immediate_subfiles


class Plugin():
    """Data structure defining a plugin, i.e., a set of pypes."""

    def __init__(self, plugin_config):
        if 'path' in plugin_config:
            # external pype
            self.name = plugin_config['name']
            self.internal = False
            self.abspath = path.join(
                path.abspath(plugin_config['path']), self.name)
            syspath.append(path.abspath(plugin_config['path']))
        else:
            # internal pype
            self.name = 'pype.' + plugin_config['name']
            self.internal = True
            self.abspath = path.join(path.dirname(
                __file__), plugin_config['name'])
        try:
            self.module = importlib.import_module(self.name)
        except ModuleNotFoundError as e:
            raise PypeException(e)
        self.doc = self.get_docu_or_default(self.module)
        self.pypes = [
            Pype(path.join(self.abspath, subfile),
                 subfile, plugin_config)
            for subfile in
            get_immediate_subfiles(self.abspath, r'^(?!__).*(?!__)\.py$')
        ]

    def get_docu_or_default(self, module):
        return (
            sub(r'[\.]+$', '', module.__doc__)  # replace trailing dots
            if module.__doc__ else 'Not documented yet'
        )
