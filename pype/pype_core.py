# -*- coding: utf-8 -*-

from importlib import import_module
from os import environ, remove
from os.path import abspath, basename, dirname, expanduser, isfile, join
from re import sub
from shutil import copyfile
from sys import path as syspath

from pype.plugin_type import Plugin
from pype.pype_config import PypeConfig
from pype.pype_exception import PypeException
from pype.util.iotools import resolve_path
from pype.util.misc import get_from_json_or_default


class PypeCore():
    """Pype core initializer."""

    SHELL_INIT_PREFIX = '.pype-initfile'
    SUPPORTED_SHELLS = {
        'bash': {
            'init_file': join(expanduser('~'), SHELL_INIT_PREFIX + '-bash'),
            'source_cmd': 'eval "$(_PYPE_COMPLETE=source pype)"'
        },
        'zsh': {
            'init_file': join(expanduser('~'), SHELL_INIT_PREFIX + '-zsh'),
            'source_cmd': 'eval "$(_PYPE_COMPLETE=source_zsh pype)"'
        }
    }

    def __init__(self):
        self.set_environment_variables()
        self.config = PypeConfig()
        # load all external plugins
        self.plugins = [
            Plugin(plugin)
            for plugin in get_from_json_or_default(
                self.config.get_json(), 'plugins', [])
        ]
        # filter plugins not valid for current environment
        self.plugins = [plugin for plugin in self.plugins if plugin.active]
        # append internal plugins
        self.plugins.append(Plugin({
            'name': 'config'
        }))

    def set_environment_variables(self):
        environ['LC_ALL'] = 'C.UTF-8'
        environ['LANG'] = 'C.UTF-8'

    def get_plugins(self):
        return self.plugins

    def get_config_json(self):
        return self.config.get_json()

    def set_config_json(self, json):
        self.config.set_json(json)

    def get_config_filepath(self):
        return self.config.get_filepath()

    def list_pypes(self):
        for plugin in self.plugins:
            print('PLUGIN: {} ({}) @ {}'.format(
                plugin.name.upper(), plugin.doc, plugin.abspath))
            for pype in plugin.pypes:
                print('\t{} - {}'.format(
                    pype.name, pype.doc
                ))
            print()

    def create_pype(self, pype_name, plugin):
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

    def delete_pype(self, pype_name, plugin):
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

    def get_abspath_to_pype(self, plugin, name):
        for pype in plugin.pypes:
            if name == pype.name:
                return pype.abspath
        return None

    def install_to_shell(self, shell_config):
        config_json = self.config.get_json()
        init_file = get_from_json_or_default(
            config_json, 'initfile', shell_config['init_file'])
        aliases = get_from_json_or_default(config_json, 'aliases', [])
        print('Writing init-file', init_file)
        with open(resolve_path(init_file), 'w+') as ifile:
            # Write pype sourcing command
            ifile.write('if [ ! -z "$( command -v pype )" ]; then\n')
            ifile.write('\t' + shell_config['source_cmd'] + '\n')
            # Write configured aliases
            for alias in aliases:
                alias_cmd = '\talias {}="{}"\n'.format(alias, aliases[alias])
                ifile.write(alias_cmd)
            ifile.write('fi\n')
        # Only add source link to target file if not present yet
        target_file = shell_config.get('target_file', None)
        if not target_file:
            return
        try:
            rc_file_content = open(
                target_file, 'r').readlines()
        except FileNotFoundError:
            rc_file_content = []
        already_present = [line for line in rc_file_content
                           if basename(init_file) in line]
        if not already_present:
            print('Adding init-file sourcing to', target_file)
            with open(target_file, 'a+') as rc_file_handle:
                rc_file_handle.write('. ' + init_file + '\n')

    def uninstall_from_shell(self, shell_config):
        if isfile(shell_config['init_file']):
            remove(shell_config['init_file'])
        if not isfile(shell_config['target_file']):
            return
        with open(shell_config['target_file'], 'r') as f:
            lines = f.readlines()
        with open(shell_config['target_file'], 'w') as f:
            for line in lines:
                if self.SHELL_INIT_PREFIX not in line.strip('\n'):
                    f.write(line)

    def register_alias(self, ctx, extra_args, alias):
        if not alias:
            return
        cmd_line = ctx.command_path + ' '.join(extra_args)
        alias_cmd = '{}="{}"'.format(alias, cmd_line)
        # store to internal config
        config_json = self.config.get_json()
        if not config_json.get('aliases', None):
            config_json['aliases'] = {}
        if config_json.get('aliases').get(alias, None):
            print('Alias already registered.')
            return
        config_json.get('aliases')[alias] = cmd_line
        self.config.set_json(config_json)
        # update install script
        self.install_to_shell(self.get_shell_config())
        print('Installed alias \'{}\''.format(alias_cmd))

    def unregister_alias(self, alias):
        if not alias:
            return
        # store to internal config
        config_json = self.config.get_json()
        if not config_json.get('aliases', None):
            print('No aliases registered.')
            return
        if not config_json.get('aliases').get(alias, None):
            print('Alias not registered.')
            return
        del config_json['aliases'][alias]
        self.config.set_json(config_json)
        # update install script
        self.install_to_shell(self.get_shell_config())
        print('Uninstalled alias \'{}\''.format(alias))

    def get_shell_config(self):
        shell = basename(environ.get('SHELL', None))
        if not any(
            [supported for supported in self.SUPPORTED_SHELLS
             if shell == supported]
        ):
            print('Unsupported shell \'{}\'.'.format(shell))
            return None
        return self.SUPPORTED_SHELLS[shell]


def load_module(name, path):
    syspath.append(abspath(path))
    try:
        return import_module(name)
    except ModuleNotFoundError as e:
        raise PypeException(e)


def get_pype_basepath():
    return dirname(dirname(__file__))
