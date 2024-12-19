# -*- coding: utf-8 -*-
"""Pype core initializer."""

import logging
import sys
from importlib import import_module
from os import environ, path, remove
from re import sub
from typing import Any, List, Optional

from click import Context
from colorama import Fore, Style
from tabulate import tabulate

from pype.config_handler import PypeConfigHandler
from pype.config_model import (Configuration, ConfigurationAlias,
                               ConfigurationPlugin)
from pype.constants import ENV_CONFIG_FOLDER
from pype.errors import PypeError
from pype.type_plugin import Plugin
from pype.util.benchmark import Benchmark
from pype.util.cli import print_error, print_success, print_warning
from pype.util.iotools import open_with_default, resolve_path


class PypeCore:
    """Pype core initializer."""

    SHELL_INIT_PREFIX = 'initfile-'
    SHELL_COMPLETE_PREFIX = 'complete-'
    SHELL_RC_HINT = '# pype-cli'

    def __init__(self) -> None:
        """Public constructor."""
        self.__set_environment_variables()
        self.__config = PypeConfigHandler()
        self.__setup_logging(self.__config)
        self.__rc_files = [
            resolve_path('~/.bashrc'),
            resolve_path('~/.bash_profile'),
            resolve_path('~/.zshrc')
        ]
        # Configure if executed in virtual environment
        if in_virtualenv():
            self.__rc_files = [
                resolve_path('./.venv/bin/activate')
            ]
        Benchmark.print_info('Loading plugin information')
        self.plugins = [
            Plugin(plugin, self.__config.get_file_path())
            for plugin in self.__config.get_config().plugins
        ]
        # filter plugins not valid for current environment
        self.plugins = [plugin for plugin in self.plugins if plugin.active]
        # append internal plugins
        self.plugins.append(Plugin(
            ConfigurationPlugin('config', '%INTERNAL%'),
            self.__config.get_file_path())
        )
        Benchmark.print_info('Plugins loaded')

    def get_plugins(self) -> List[Plugin]:
        """Get list of configured plugins."""
        return self.plugins

    def open_config_with_default(self) -> None:
        """Get absolute filepath to configuration JSON file."""
        return open_with_default(self.__config.get_file_path())

    def list_pypes(self) -> None:
        """Print list of pypes to console."""
        for plugin in self.plugins:
            built_in = 'Built-in' if plugin.internal else plugin.abspath
            print(f'{Style.BRIGHT}{Fore.BLUE}'
                  f'PLUGIN: {plugin.name.upper()}{Fore.LIGHTBLACK_EX}\n'
                  f'{plugin.doc}\n@ {built_in}'
                  )
            print(f'{Style.BRIGHT}{Fore.BLUE}– PYPES:')
            for pype in plugin.pypes:
                pype_name = sub('_', '-', pype.name)
                print(
                    f'  {Style.BRIGHT}{Fore.BLUE}{pype_name}'
                    f'{Style.RESET_ALL} – {pype.doc}'
                )
            print()

    def get_aliases(self) -> List[str]:
        """Return available aliases."""
        aliases = self.__config.get_config().aliases
        return sorted([alias.alias for alias in aliases])

    def print_aliases(self) -> None:
        """Print list of aliases to console."""
        aliases = self.__config.get_config().aliases
        sorted_alias_keys = sorted([alias.alias for alias in aliases])
        alias_table = []

        for alias in sorted_alias_keys:
            find_alias = self.__find_alias(aliases, alias)
            alias_table.append([
                f'{Style.BRIGHT}{Fore.BLUE}{alias}',
                Style.RESET_ALL + '=',
                f'{Style.BRIGHT}{Fore.LIGHTBLACK_EX}{find_alias}'
            ])
        print(tabulate(alias_table, tablefmt='plain'))

    def install_to_shell(self) -> None:
        """Install shell features."""
        # Clean up first
        self.uninstall_from_shell()
        print_success('Successfully cleaned up existing configurations')
        aliases = self.__config.get_config().aliases
        self.__write_init_file('bsh', aliases)
        self.__write_init_file('zsh', aliases)
        print('Add link to init-file in rc-files if present')
        for file in self.__rc_files:
            if not path.isfile(file):
                continue
            print(f' - "{file}"')
            # Append link to init-file and set config file
            file_handle = open(file, 'a+')
            init_file = path.join(
                self.__config.get_dir_path(), self.SHELL_INIT_PREFIX)
            init_file = (init_file + 'zsh' if 'zshrc' in file
                         else init_file + 'bsh')
            config_path = resolve_path(self.__config.get_dir_path())
            file_handle.write(
                f'export {ENV_CONFIG_FOLDER}="{config_path}" '
                f'{self.SHELL_RC_HINT}\n'
            )
            file_handle.write(f'. {init_file} {self.SHELL_RC_HINT}\n')
            file_handle.close()
            if in_virtualenv():
                print('Running in .venv. Skipping system rc files.')
                break
        print_success('Successfully written init-files')

    def uninstall_from_shell(self) -> None:
        """Uninstall shell features."""
        # Remove init files
        cfg_dir = self.__config.get_dir_path()
        for file in [
            path.join(cfg_dir, self.SHELL_INIT_PREFIX + 'bsh'),
            path.join(cfg_dir, self.SHELL_INIT_PREFIX + 'zsh'),
            path.join(cfg_dir, self.SHELL_COMPLETE_PREFIX + 'bsh'),
            path.join(cfg_dir, self.SHELL_COMPLETE_PREFIX + 'zsh')
        ]:
            self.__remove_file_silently(file)
        print('Remove link to init-file from rc-files if present')
        for file in self.__rc_files:
            if not path.isfile(file):
                continue
            file_handle = open(file, 'r')
            content = file_handle.readlines()
            file_handle.close()
            # Don't rewrite if rc file does not link to initfile
            if not any(list(filter(
                    lambda x: self.SHELL_RC_HINT in str(x), content
            ))):
                continue
            # Delete initfile-links from rc file
            print(f' - "{file}"')
            file_handle = open(file, 'w')
            [file_handle.write(cn)
             for cn in content if self.SHELL_RC_HINT not in cn]
            file_handle.close()
            if hasattr(sys, 'real_prefix'):
                print('Running in .venv. Skipping system rc files.')
                break

    def alias_register(self, ctx: Any) -> None:
        """Register a new alias."""
        alias = ctx.parent.alias_register
        # Combine the current context's command path with remaining CL-args
        cmd_path = ctx.command_path.split(' ')
        cmd_path_last = cmd_path[-1]
        found_entry = False
        for arg in sys.argv:
            if found_entry:
                cmd_path.append(arg)
            if arg.strip() == cmd_path_last:
                found_entry = True
        cmd_line = ' '.join(cmd_path)
        if not alias:
            return
        alias_cmd = f'{alias}="{cmd_line.strip()}"'
        # store to internal config
        config = self.__config.get_config()
        if self.__alias_present(config, alias):
            print_warning('Alias already registered.')
            return
        config.aliases.append(ConfigurationAlias(alias, cmd_line))
        print_success(f'Configured alias: {alias_cmd}')
        self.__config.set_config(config)
        # update install script
        self.install_to_shell()

    def alias_unregister(self, alias: str) -> None:
        """Unregister the provided alias."""
        if not alias:
            return
        # store to internal config
        config = self.__config.get_config()
        if not config.aliases:
            print_warning('No aliases registered.')
            exit(1)
        if not self.__alias_present(config, alias):
            print_warning('Alias not registered.')
            exit(1)
        for obj in enumerate(config.aliases):
            if obj[1].alias != alias:
                continue
            del config.aliases[obj[0]]
        self.__config.set_config(config)
        # update install script
        print_success(f'Unregistered alias: {alias}')
        self.install_to_shell()

    def __write_init_file(self, init_file: str, aliases: List) -> None:
        shell_command = path.basename(sys.argv[0])
        cfg_dir = self.__config.get_dir_path()
        source_cmd = 'zsh_source' if init_file == 'zsh' else 'bash_source'
        target_file = resolve_path(
            path.join(cfg_dir, self.SHELL_INIT_PREFIX + init_file)
        )
        complete_file = resolve_path(
            path.join(cfg_dir, self.SHELL_COMPLETE_PREFIX + init_file)
        )
        target_handle = open(resolve_path(target_file), 'w+')
        print('Writing init-file ' + target_file)
        alias_definition = ''.join([
            f'\talias {alias.alias}="{alias.command}"\n'
            for alias in aliases
        ])
        console_script = path.dirname(sys.argv[0])
        shell_upper = shell_command.upper()
        target_handle.write(f"""# PYPE-CLI INIT-FILE: {init_file}
export PATH=$PATH:{console_script}
if [ ! -z "$( command -v {shell_command} )" ] # Only if installed
then
    if [ ! -s {complete_file} ]
    then
        _{shell_upper}_COMPLETE={source_cmd} {shell_command} > {complete_file}
    fi
    . {complete_file}

{alias_definition}
fi
""")

    @staticmethod
    def create_pype_or_exit(
        pype_name: str,
        plugin: Plugin,
        minimal: bool
    ) -> str:
        """Create a new pype inside the given plugin."""
        if plugin.internal:
            print_error('Creating internal pypes is not supported.')
            exit(1)
        # Normalize filename to be PEP8-conform
        target_name = sub('-', '_', sub(r'\.py$', '', pype_name))
        # Create absolute path
        target_file = path.join(plugin.abspath, target_name + '.py')
        if path.isfile(target_file):
            print_warning('Pype already present')
            exit(1)
        # Depending on user input create a documented or simple template
        template_name = ('template_minimal.py' if minimal
                         else 'template.py')
        source_file = path.join(path.dirname(__file__), template_name)
        source_handle = open(source_file, 'r', encoding='utf-8')
        target_handle = open(target_file, 'w+', encoding='utf-8')
        for line in source_handle.readlines():
            if r'%%PYPE_NAME%%' in line:
                line = sub(r'%%PYPE_NAME%%', pype_name, line)
            target_handle.write(line)
        source_handle.close()
        target_handle.close()
        print_success('Created new pype ' + target_file)
        return target_file

    @staticmethod
    def delete_pype(pype_name: str, plugin: Plugin) -> None:
        """Delete pype from the given plugin."""
        if plugin.internal:
            print_error('Deleting internal pypes is not supported.')
            exit(1)
        source_name = sub('-', '_', sub(r'\.py$', '', pype_name))
        source_name = path.join(plugin.abspath, source_name + '.py')
        try:
            remove(source_name)
        except FileNotFoundError:
            print_error('No such pype')
            exit(1)
        print_success('Deleted pype ' + source_name)

    @staticmethod
    def get_abspath_to_pype(plugin: Plugin, name: str) -> Optional[str]:
        """Get absoulte path to pype Python script."""
        for pype in plugin.pypes:
            if name == pype.name:
                return pype.abspath
        return None

    @staticmethod
    def __remove_file_silently(target_file: str) -> None:
        target_file = resolve_path(target_file)
        print('Removing init-file ' + target_file)
        try:
            remove(target_file)
        except FileNotFoundError:
            pass  # Silent ignore to make function idempotent

    @staticmethod
    def __set_environment_variables() -> None:
        environ['LC_ALL'] = 'C.UTF-8'
        environ['LANG'] = 'C.UTF-8'

    @staticmethod
    def __find_alias(
        aliases: List[ConfigurationAlias],
        key: str
    ) -> Optional[ConfigurationAlias]:
        for alias in aliases:
            if key == alias.alias:
                return alias
        return None

    @staticmethod
    def __alias_present(config: Configuration, alias: str) -> bool:
        return any([
            existing_alias
            for existing_alias in config.aliases
            if existing_alias.alias == alias
        ])

    @staticmethod
    def __setup_logging(config: PypeConfigHandler) -> None:
        log_cfg = config.get_core_config_logging()
        if not log_cfg or not log_cfg.enabled:
            return
        logging.basicConfig(
            level=str(log_cfg.level),
            format=log_cfg.pattern,
            filename=path.join(log_cfg.directory, 'pype-cli.log')
        )
        logging.getLogger('pype-cli')


def load_module(name: str, module_path: str) -> Any:
    """Try to import the module at the provided path using classloader."""
    sys.path.append(path.abspath(module_path))
    try:
        return import_module(name)
    # This used to be a ModuleNotFoundException but it's only Python >= 3.6
    except Exception as e:  # noqa: F821
        raise PypeError(e)


def get_pype_basepath() -> str:
    """Get directory filename of this pype installation."""
    return path.dirname(path.dirname(__file__))


def print_context_help(ctx: Context, level: int = 0) -> None:
    """Print help page for current context with some slight improvements."""
    default_help = ctx.get_help()
    if level == 1:
        print(sub('Commands:', 'Plugins:', default_help))
    elif level == 2:
        print(sub('Commands:', 'Pypes:', default_help))
    else:
        print(default_help)


def get_base_prefix_compat() -> str:
    """Get base/real prefix, or sys.prefix if there is none."""
    return getattr(sys, 'base_prefix', None) or \
        getattr(sys, 'real_prefix', None) or sys.prefix


def in_virtualenv() -> bool:
    """Return True when pype is executed inside a virtual env."""
    return (
        hasattr(sys, 'real_prefix')
        or (
            hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
        )
    )
