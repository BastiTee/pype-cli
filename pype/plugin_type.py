#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import importlib
import inspect
from os import path
from re import sub

from pype.exceptions import PypeConfigurationException
from pype.pype_type import Pype
from pype.util.iotools import get_immediate_subfiles


class Plugin():

    def __init__(self, plugin_name):
        try:
            py_module = importlib.import_module(plugin_name)
        except ModuleNotFoundError as e:
            raise PypeConfigurationException(e)
        self.name = plugin_name
        self.module = py_module
        self.abspath = path.dirname(inspect.getabsfile(py_module))
        self.pypes = [
            Pype(path.join(self.abspath, subfile), subfile, plugin_name)
            for subfile in
            get_immediate_subfiles(self.abspath, r'^(?!__).*(?!__)\.py$')
        ]
        self.doc = self.get_docu_or_default(py_module)

    def get_docu_or_default(self, module):
        return (
            sub(r'[\.]+$', '', module.__doc__)  # replace trailing dots
            if module.__doc__ else 'Not documented yet'
        )
