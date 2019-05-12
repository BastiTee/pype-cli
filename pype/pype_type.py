#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

from os import path
from re import sub


class Pype():

    def __init__(self, abspath, filename, pype_name):
        self.name = sub(r'\.py$', '', filename)
        self.abspath = abspath
        self.docu = self.get_module_docstring(self.abspath)
        # pype = {
        #     'name':
        #     'doc': self.get_module_docstring(abspath_cmd)
        # }
        # pypes.append(pype)

    def get_module_docstring(self, filepath):
        """Get module-level docstring of Python module at filepath."""
        co = compile(open(filepath).read(), filepath, 'exec')
        if co.co_consts and isinstance(co.co_consts[0], str):
            return sub(r'[\.]+$', '', co.co_consts[0])
        return 'Not documented yet'
