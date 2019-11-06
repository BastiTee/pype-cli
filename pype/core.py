# -*- coding: utf-8 -*-
"""Pype core initializer."""

from importlib import import_module
from os import environ, remove
from os.path import abspath, basename, dirname, isfile, join
from re import sub
from shutil import copyfile
from sys import argv, path as syspath

from colorama import Fore, Style

from pype.config_handler import PypeConfigHandler
from pype.constants import ENV_CONFIG_FILE, ENV_TEST_CONFIG_FILE
from pype.exceptions import PypeException
from pype.type_plugin import Plugin
from pype.util.cli import print_error, print_success, print_warning
from pype.util.iotools import resolve_path

from tabulate import tabulate


class PypeCore:
    """Pype core initializer."""

    SHELL_INIT_PREFIX = '.pype-initfile-'
    SHELL_COMPLETE_PREFIX = '.pype-complete-'

    def __init__(self):
        """Public constructor."""
        self.__set_environment_variables()
        # Check if pype-cli is currently under test Volkswagen-style
        test_config_file = environ.get(ENV_TEST_CONFIG_FILE, None)
        self.__config = PypeConfigHandler(test_config_file)
        self.__test_postfix = '-test' if test_config_file else ''
        self.__rc_files = [
            resolve_path('~/.bashrc' + self.__test_postfix),
            resolve_path('~/.bash_profile' + self.__test_postfix),
            resolve_path('~/.zshrc' + self.__test_postfix)
        ]
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
                Style.BRIGHT, Fore.BLUE, plugin.name.upper(),
                Fore.LIGHTBLACK_EX, plugin.doc,
                'Built-in' if plugin.internal else plugin.abspath))
            print('{}{}– PYPES:'.format(Style.BRIGHT, Fore.BLUE))
            for pype in plugin.pypes:
                print('  {}{}{}{} – {}'.format(
                    Style.BRIGHT, Fore.BLUE, sub('_', '-', pype.name),
                    Style.RESET_ALL, pype.doc
                ))
            print()

    def list_aliases(self):
        """Print list of aliases to console."""
        aliases = self.get_config_json().get('aliases')
        sorted_alias_keys = sorted([alias['alias'] for alias in aliases])
        alias_table = []

        for alias in sorted_alias_keys:
            alias_table.append([
                '{}{}{}'.format(Style.BRIGHT, Fore.BLUE, alias),
                Style.RESET_ALL + '=',
                '{}{}{}'.format(Style.BRIGHT, Fore.LIGHTBLACK_EX,
                                self._find_alias(aliases, alias)['command'])
            ])
        print(tabulate(alias_table, tablefmt='plain'))

    def __write_init_file(self, init_file, aliases):
        shell_command = basename(argv[0])
        source_cmd = 'source_zsh' if init_file == 'zsh' else 'source'
        target_file = resolve_path(
            '~/' + self.SHELL_INIT_PREFIX + init_file
            + self.__test_postfix)
        complete_file = resolve_path(
            '~/' + self.SHELL_COMPLETE_PREFIX + init_file
            + self.__test_postfix)
        target_handle = open(resolve_path(target_file), 'w+')
        print('Writing init-file ' + target_file)
        target_handle.write("""# PYPE-CLI INIT-FILE: {}
export PATH=$PATH:{}
if [ ! -z "$( command -v {} )" ] # Only if installed
then
    if [ ! -f {} ]
    then
        _{}_COMPLETE={} {} > {}
    fi
    . {}

{}
fi
""".format(
            init_file,  # Init-file descriptor
            dirname(argv[0]),  # Path to console script
            shell_command,  # Configured shell command
            complete_file,  # Complete file name
            shell_command.upper(),  # Configured shell command upper case
            source_cmd,  # Sourcing command,
            shell_command,  # Configured shell command
            complete_file,  # Complete file name
            complete_file,  # Complete file name
            ''.join([
                '\talias {}="{}"\n'.format(alias['alias'], alias['command'])
                for alias in aliases
            ])  # Alias definitions
        ))

    def install_to_shell(self):
        """Install shell features."""
        # Clean up first
        self.uninstall_from_shell()
        print_success('Successfully cleaned up existing configurations')
        config_json = self.__config.get_json()
        aliases = get_from_json_or_default(config_json, 'aliases', [])
        self.__write_init_file('bsh', aliases)
        self.__write_init_file('zsh', aliases)
        print('Add link to init-file in rc-files if present')
        for file in self.__rc_files:
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
        print_success('Successfully written init-files')

    def uninstall_from_shell(self):
        """Uninstall shell features."""
        # Remove init files
        for file in [
            '~/' + self.SHELL_INIT_PREFIX + 'bsh' + self.__test_postfix,
            '~/' + self.SHELL_INIT_PREFIX + 'zsh' + self.__test_postfix,
            '~/' + self.SHELL_COMPLETE_PREFIX + 'bsh' + self.__test_postfix,
            '~/' + self.SHELL_COMPLETE_PREFIX + 'zsh' + self.__test_postfix
        ]:
            self.__remove_file_silently(file)
        print('Remove link to init-file from rc-files if present')
        for file in self.__rc_files:
            if not isfile(file):
                continue
            file_handle = open(file, 'r')
            content = file_handle.readlines()
            file_handle.close()
            # Don't rewrite if rc file does not link to initfile
            if not any(
                list(filter(
                    lambda x: self.SHELL_INIT_PREFIX in x, content))):
                continue
            # Delete initfile-links from rc file
            print(' - "{}"'.format(file))
            file_handle = open(file, 'w')
            [file_handle.write(cn)
             for cn in content if self.SHELL_INIT_PREFIX not in cn]
            file_handle.close()

    def register_alias(self, ctx):
        """Register a new alias."""
        alias = ctx.parent.register_alias
        # Combine the current context's command path with remaining CL-args
        cmd_path = ctx.command_path.split(' ')
        cmd_path_last = cmd_path[-1]
        found_entry = False
        for arg in argv:
            if found_entry:
                cmd_path.append(arg)
            if arg.strip() == cmd_path_last:
                found_entry = True
        cmd_line = ' '.join(cmd_path)
        if not alias:
            return
        alias_cmd = '{}="{}"'.format(alias, cmd_line.strip())
        # store to internal config
        config_json = self.__config.get_json()
        if not config_json.get('aliases', None):
            config_json['aliases'] = []
        if self._alias_present(config_json, alias):
            print_warning('Alias already registered.')
            return
        config_json.get('aliases').append({
            'alias': alias,
            'command': cmd_line
        })
        print_success('Configured alias: {}'.format(alias_cmd))
        self.__config.set_json(config_json)
        # update install script
        self.install_to_shell()

    def unregister_alias(self, alias):
        """Unregister the provided alias."""
        if not alias:
            return
        # store to internal config
        config_json = self.__config.get_json()
        if not config_json.get('aliases', None):
            print_warning('No aliases registered.')
            exit(1)
        if not self._alias_present(config_json, alias):
            print_warning('Alias not registered.')
            exit(1)
        for obj in enumerate(config_json['aliases']):
            if obj[1]['alias'] != alias:
                continue
            del config_json['aliases'][obj[0]]
        self.__config.set_json(config_json)
        # update install script
        print_success('Unregistered alias: {}'.format(alias))
        self.install_to_shell()

    def get_core_config(self, key, default=None):
        """Return a key from the core configuration of the config file."""
        return get_from_json_or_default(
            self.get_config_json(), 'core_config.' + key, default)

    @staticmethod
    def _find_alias(aliases, key):
        for alias in aliases:
            if key == alias['alias']:
                return alias

    @staticmethod
    def _alias_present(config_json, alias):
        return any(
            [existing_alias for existing_alias in config_json.get('aliases')
             if existing_alias['alias'] == alias])

    @staticmethod
    def create_pype_or_exit(pype_name, plugin, minimal):
        """Create a new pype inside the given plugin."""
        if plugin.internal:
            print_error('Creating internal pypes is not supported.')
            exit(1)
        # Normalize filename to be PEP8-conform
        target_name = sub('-', '_', sub(r'\.py$', '', pype_name))
        # Create absolute path
        target_file = join(plugin.abspath, target_name + '.py')
        if isfile(target_file):
            print_warning('Pype already present')
            exit(1)
        # Depending on user input create a documented or simple template
        template_name = ('template_minimal.py' if minimal
                         else 'template.py')
        source_name = join(dirname(__file__), template_name)
        copyfile(source_name, target_file)
        print_success('Created new pype ' + target_file)
        return target_file

    @staticmethod
    def delete_pype(pype_name, plugin):
        """Delete pype from the given plugin."""
        if plugin.internal:
            print_error('Deleting internal pypes is not supported.')
            exit(1)
        source_name = sub('-', '_', sub(r'\.py$', '', pype_name))
        source_name = join(plugin.abspath, source_name + '.py')
        try:
            remove(source_name)
        except FileNotFoundError:
            print_error('No such pype')
            exit(1)
        print_success('Deleted pype ' + source_name)

    @staticmethod
    def get_abspath_to_pype(plugin, name):
        """Get absoulte path to pype Python script."""
        for pype in plugin.pypes:
            if name == pype.name:
                return pype.abspath
        return None

    @staticmethod
    def __remove_file_silently(target_file):
        target_file = resolve_path(target_file)
        print('Removing init-file ' + target_file)
        try:
            remove(target_file)
        except FileNotFoundError:
            pass  # Silent ignore to make function idempotent

    @staticmethod
    def __set_environment_variables():
        environ['LC_ALL'] = 'C.UTF-8'
        environ['LANG'] = 'C.UTF-8'


def get_from_json_or_default(json, path, default_value):
    """Try to load a key breadcrumb from a JSON object or return default."""
    if not path:
        return default_value
    json = json if json else {}
    try:
        for breadcrumb in path.split('.'):
            json = json[breadcrumb]
        return json if json else default_value
    except KeyError:
        return default_value


def load_module(name, path):
    """Try to import the module at the provided path using classloader."""
    syspath.append(abspath(path))
    try:
        return import_module(name)
    # This used to be a ModuleNotFoundException but it's only Python >= 3.6
    except Exception as e:  # noqa: F821
        raise PypeException(e)


def get_pype_basepath():
    """Get directory filename of this pype installation."""
    return dirname(dirname(__file__))


def print_context_help(ctx, level=0):
    """Print help page for current context with some slight improvements."""
    default_help = ctx.get_help()
    if level == 1:
        print(sub('Commands:', 'Plugins:', default_help))
    elif level == 2:
        print(sub('Commands:', 'Pypes:', default_help))
    else:
        print(default_help)
