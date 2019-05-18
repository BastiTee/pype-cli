# -*- coding: utf-8 -*-

from json import load
from os.path import dirname

from pype.plugin_type import Plugin
from pype.util.misc import get_or_default


class PypeCore():
    """Pype core initializer."""

    def __init__(self, config_file):
        self.plugins = [
            Plugin(plugin)
            for plugin in get_or_default(
                load(open(config_file, 'r')), 'plugins', [])
        ]

    def get_plugins(self):
        return self.plugins

    def list_pypes(self):
        for plugin in self.plugins:
            print('PLUGIN: {} ({}) @ {}'.format(
                plugin.name.upper(), plugin.doc, plugin.abspath))
            for pype in plugin.pypes:
                print('\t{} - {}'.format(
                    pype.name, pype.doc
                ))
            print()


def get_pype_basepath():
    return dirname(dirname(__file__))
