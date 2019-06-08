# -*- coding: utf-8 -*-
"""Pype core initializer."""

from importlib import import_module
from os import environ, remove
from os.path import abspath, dirname, isfile, join
from re import sub
from shutil import copyfile
from sys import path as syspath

from colorama import Fore, Style

from pype.config_handler import PypeConfigHandler
from pype.constants import ENV_CONFIG_FILE
from pype.exceptions import PypeException
from pype.type_plugin import Plugin
from pype.util.iotools import resolve_path
from pype.util.misc import get_from_json_or_default

from tabulate import tabulate


class PypeCore():
    """Pype core initializer."""

    def __init__(self):
        """Public constructor."""
        self.__set_environment_variables()
        self.__config = PypeConfigHandler()
        # load all external plugins
        self.plugins = [
            Plugin(plugin, self.get_config_filepath())
            for plugin in get_from_json_or_default(
                self.__config.get_json(), 'plugins', [])
        ]
        # filter plugins not valid for current environment
        self.plugins = [plugin for plugin in self.plugins if plugin.active]
        # append internal plugins
        self.plugins.append(Plugin({
            'name': 'config',
            'users': []
        }, self.get_config_filepath()))

    def __set_environment_variables(self):
        environ['LC_ALL'] = 'C.UTF-8'
        environ['LANG'] = 'C.UTF-8'

    def get_plugins(self):
        """Get list of configured plugins."""
        return self.plugins

    def get_config_json(self):
        """Get pype configuration as JSON object."""
        return self.__config.get_json()

    def set_config_json(self, json):
        """Set configuration from JSON object."""
        self.__config.set_json(json)

    def get_config_filepath(self):
        """Get absolute filepath to configuration JSON file."""
        return self.__config.get_filepath()

    def list_pypes(self):
        """Print list of pypes to console."""
        for plugin in self.plugins:
            print('{}{}PLUGIN: {}{}\n{}\n@ {}'.format(
                Style.BRIGHT, Fore.RED, plugin.name.upper(),
                Fore.LIGHTBLACK_EX, plugin.doc,
                'Built-in' if plugin.internal else plugin.abspath))
            print('{}{}– PYPES:'.format(Style.BRIGHT, Fore.RED))
            for pype in plugin.pypes:
                print('  {}{}{}{} – {}'.format(
                    Style.BRIGHT, Fore.RED, sub('_', '-', pype.name),
                    Style.RESET_ALL, pype.doc
                ))
            print()

    def list_aliases(self):
        """Print list of aliases to console."""
        aliases = self.get_config_json().get('aliases')
        sorted_alias_keys = sorted([alias['alias'] for alias in aliases])
        alias_table = []

        def find_alias(aliases, key):
            for alias in aliases:
                if key == alias['alias']:
                    return alias

        for alias in sorted_alias_keys:
            alias_table.append([
                '{}{}{}'.format(Style.BRIGHT, Fore.RED, alias),
                Style.RESET_ALL + '=',
                '{}{}{}'.format(Style.BRIGHT, Fore.LIGHTBLACK_EX,
                                find_alias(aliases, alias)['command'])
            ])
        print(tabulate(alias_table, tablefmt='plain'))

    def create_pype_or_exit(self, pype_name, plugin, minimal):
        """Create a new pype inside the given plugin."""
        if plugin.internal:
            print('Creating internal pypes is not supported.')
            exit(1)
        # Normalize filename to be PEP8-conform
        target_name = sub('-', '_', sub(r'\.py$', '', pype_name))
        # Create absolute path
        target_file = join(plugin.abspath, target_name + '.py')
        if isfile(target_file):
            print('Pype already present')
            exit(1)
        # Depending on user input create a documented or simple template
        template_name = ('template_minimal.py' if minimal
                         else 'template.py')
        source_name = join(dirname(__file__), template_name)
        copyfile(source_name, target_file)
        print('Created new pype', target_file)
        return target_file

    def delete_pype(self, pype_name, plugin):
        """Delete pype from the given plugin."""
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
        """Get absoulte path to pype Python script."""
        for pype in plugin.pypes:
            if name == pype.name:
                return pype.abspath
        return None

    SHELL_INIT_PREFIX = '.pype-initfile-'
    SUPPORTED_RC_FILES = [
        resolve_path('~/.bashrc'),
        resolve_path('~/.bash_profile'),
        resolve_path('~/.zshrc')
    ]

    def __write_init_file(self, init_file, shell_command, aliases):
        target_file = resolve_path('~/' + self.SHELL_INIT_PREFIX + init_file)
        print('Writing init-file', target_file)
        with open(resolve_path(target_file), 'w+') as ifile:
            # Write pype sourcing command
            ifile.write('if [ ! -z "$( command -v '
                        + shell_command
                        + ' )" ]; then\n')
            source_cmd = 'eval "$(_{}_COMPLETE=source{} {})"'.format(
                shell_command.upper(),
                '_zsh' if init_file == 'zsh' else '',
                shell_command
            )
            ifile.write('\t' + source_cmd + '\n')
            # Write configured aliases
            for alias in aliases:
                alias_cmd = '\talias {}="{}"\n'.format(
                    alias['alias'], alias['command'])
                ifile.write(alias_cmd)
            # Close if
            ifile.write('fi\n')

    def __remove_init_file(self, init_file):
        target_file = resolve_path('~/' + self.SHELL_INIT_PREFIX + init_file)
        print('Removing init-file', target_file)
        try:
            remove(target_file)
        except FileNotFoundError:
            pass  # Silent ignore to make function idempotent

    def install_to_shell(self):
        """Install shell features."""
        # Clean up first
        self.uninstall_from_shell()
        # Write new init-files
        config_json = self.__config.get_json()
        shell_command = self.get_core_config('shell_command', 'pype')
        aliases = get_from_json_or_default(config_json, 'aliases', [])
        print('Using shell command "{}"'.format(shell_command))
        self.__write_init_file('bsh', shell_command, aliases)
        self.__write_init_file('zsh', shell_command, aliases)
        print('Add link to init-file in rc-files if present')
        for file in self.SUPPORTED_RC_FILES:
            if not isfile(file):
                continue
            print(' - "{}"'.format(file))
            # Append link to init-file and set config file
            file_handle = open(file, 'a+')
            init_file = '~/' + self.SHELL_INIT_PREFIX
            init_file = (init_file + 'zsh' if 'zshrc' in file
                         else init_file + 'bsh')
            file_handle.write('export {}="{}" # {}\n'.format(
                ENV_CONFIG_FILE,
                resolve_path(self.get_config_filepath()),
                self.SHELL_INIT_PREFIX
            ))
            file_handle.write('. ' + init_file + '\n')
            file_handle.close()

    def uninstall_from_shell(self):
        """Uninstall shell features."""
        # Remove init files
        self.__remove_init_file('bsh')
        self.__remove_init_file('zsh')
        print('Remove link to init-file from rc-files if present')
        for file in self.SUPPORTED_RC_FILES:
            if not isfile(file):
                continue
            file_handle = open(file, 'r')
            content = file_handle.readlines()
            file_handle.close()
            # Don't rewrite if rc file does not link to initfile
            if not any(list(filter(
                    lambda x: self.SHELL_INIT_PREFIX in x, content))):
                continue
            # Delete initfile-links from rc file
            print(' - "{}"'.format(file))
            file_handle = open(file, 'w')
            [file_handle.write(cn)
             for cn in content if self.SHELL_INIT_PREFIX not in cn]
            file_handle.close()

    def register_alias(self, ctx, extra_args, alias):
        """Register a new alias."""
        if not alias:
            return
        cmd_line = ctx.command_path + ' ' + ' '.join(extra_args)
        alias_cmd = '{}="{}"'.format(alias, cmd_line.strip())
        # store to internal config
        config_json = self.__config.get_json()
        if not config_json.get('aliases', None):
            config_json['aliases'] = []
        if self._alias_present(config_json, alias):
            print('Alias already registered.')
            return
        config_json.get('aliases').append({
            'alias': alias,
            'command': cmd_line
        })
        self.__config.set_json(config_json)
        # update install script
        self.install_to_shell()
        print('Installed alias "{}"'.format(alias_cmd))

    def unregister_alias(self, alias):
        """Unregister the provided alias."""
        if not alias:
            return
        # store to internal config
        config_json = self.__config.get_json()
        if not config_json.get('aliases', None):
            print('No aliases registered.')
            return
        if not self._alias_present(config_json, alias):
            print('Alias not registered.')
            return
        for obj in enumerate(config_json['aliases']):
            if obj[1]['alias'] != alias:
                continue
            del config_json['aliases'][obj[0]]
        self.__config.set_json(config_json)
        # update install script
        self.install_to_shell()
        print('Uninstalled alias "{}"'.format(alias))

    def _alias_present(self, config_json, alias):
        return any(
            [existing_alias for existing_alias in config_json.get('aliases')
             if existing_alias['alias'] == alias])

    def get_core_config(self, key, default=None):
        """Return a key from the core configuration of the config file."""
        return get_from_json_or_default(
            self.get_config_json(), 'core_config.' + key, default)


def load_module(name, path):
    """Try to import the module at the provided path using classloader."""
    syspath.append(abspath(path))
    try:
        return import_module(name)
    except ModuleNotFoundError as e:  # noqa: F821
        raise PypeException(e)


def get_pype_basepath():
    """Get directory filename of this pype installation."""
    return dirname(dirname(__file__))
