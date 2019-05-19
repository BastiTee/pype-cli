# -*- coding: utf-8 -*-

from importlib import import_module
from json import load, dump
from os import environ, remove
from os.path import abspath, dirname, join, isfile
from sys import path as syspath
from re import sub
from shutil import copyfile

from pype.plugin_type import Plugin
from pype.pype_exception import PypeException
from pype.util.misc import get_or_default


class PypeCore():
    """Pype core initializer."""

    def __init__(self):
        self.resolve_config_file()
        # load all external plugins
        self.plugins = [
            Plugin(plugin)
            for plugin in get_or_default(
                self.config_json, 'plugins', [])
        ]
        # append internal plugins
        self.plugins.append(Plugin({
            'name': 'config'
        }))

    def resolve_config_file(self):
        try:
            self.config_filepath = environ['PYPE_CONFIG_JSON']
        except KeyError:
            self.config_filepath = join(
                dirname(dirname(__file__)), 'config.json')
        self.config_json = load(open(self.config_filepath, 'r'))

    def get_plugins(self):
        return self.plugins

    def get_config_json(self):
        return self.config_json

    def get_config_filepath(self):
        return self.config_filepath

    def set_config_json(self, config_json):
        self.config_json = config_json
        # always update config file as well
        dump(self.config_json, open(self.config_filepath, 'w'), indent=4)

    def list_pypes(self):
        for plugin in self.plugins:
            print('PLUGIN: {} ({}) @ {}'.format(
                plugin.name.upper(), plugin.doc, plugin.abspath))
            for pype in plugin.pypes:
                print('\t{} - {}'.format(
                    pype.name, pype.doc
                ))
            print()

    def create_pype_from_template(self, pype_name, plugin):
        if plugin.internal:
            print('Creating internal pypes is not supported.')
            return
        target_name = sub('-', '_', sub(r'\.py$', '', pype_name))
        target_name = join(plugin.abspath, target_name + '.py')
        source_name = join(dirname(__file__), 'pype_template.py')
        if isfile(target_name):
            print('Pype already present')
            return
        copyfile(source_name, target_name)
        print('Created new pype', target_name)

    def delete_pype_by_name(self, pype_name, plugin):
        if plugin.internal:
            print('Deleting internal pypes is not supported.')
            return
        source_name = sub('-', '_', sub(r'\.py$', '', pype_name))
        source_name = join(plugin.abspath, source_name + '.py')
        try:
            remove(source_name)
        except FileNotFoundError:
            print('No such pype')
            return
        print('Deleted pype', source_name)


def load_module(name, path):
    syspath.append(abspath(path))
    try:
        return import_module(name)
    except ModuleNotFoundError as e:
        raise PypeException(e)


def get_pype_basepath():
    return dirname(dirname(__file__))
