# -*- coding: utf-8 -*-
"""Data structure defining a pype."""

from re import sub

from pype.constants import NOT_DOCUMENTED_YET


class Pype:
    """Data structure defining a pype."""

    def __init__(self, abspath, filename, plugin):
        """Activate pypes for the provided configuration."""
        self.name = sub(r'\.py$', '', filename)
        self.doc = self.__get_module_docstring(abspath)
        self.abspath = abspath
        self.plugin_name = plugin.name

    @staticmethod
    def __get_module_docstring(filepath):
        co = compile(open(filepath).read(), filepath, 'exec')
        if co.co_consts and isinstance(co.co_consts[0], str):
            return co.co_consts[0]
        return NOT_DOCUMENTED_YET
