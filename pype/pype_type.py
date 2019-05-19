# -*- coding: utf-8 -*-

from re import sub


class Pype():
    """Data structure defining a pype."""

    def __init__(self, abspath, filename, pype_name):
        self.name = sub(r'\.py$', '', filename)
        self.doc = self.get_module_docstring(abspath)
        self.abspath = abspath

    def get_module_docstring(self, filepath):
        co = compile(open(filepath).read(), filepath, 'exec')
        if co.co_consts and isinstance(co.co_consts[0], str):
            return sub(r'[\.]+$', '', co.co_consts[0])
        return 'Not documented yet'
