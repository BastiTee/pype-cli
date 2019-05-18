#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import importlib
from os import path
from re import sub
from sys import path as syspath

from pype.exceptions import PypeConfigurationException
from pype.pype_type import Pype
from pype.util.iotools import get_immediate_subfiles


class Plugin():

    def __init__(self, plugin_config):
        self.name = plugin_config['name']
        syspath.append(path.abspath(plugin_config['path']))
        try:
            self.module = importlib.import_module(self.name)
        except ModuleNotFoundError as e:
            raise PypeConfigurationException(e)
        self.doc = self.get_docu_or_default(self.module)
        self.abspath = path.join(
            path.abspath(plugin_config['path']), self.name)
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
