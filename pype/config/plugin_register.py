# -*- coding: utf-8 -*-
"""Register a new plugin."""

import getpass
from os import mkdir
from os.path import dirname, isdir, isfile, join
from re import IGNORECASE, sub

import click

from pype.config_handler import PypeConfigHandler
from pype.config_model import ConfigurationPlugin
from pype.constants import NOT_DOCUMENTED_YET
from pype.core import load_module
from pype.errors import PypeError
from pype.util.cli import fname_to_name, print_error, print_success
from pype.util.iotools import resolve_path


@click.command(name=fname_to_name(__file__), help=__doc__)
@click.option('--name', '-n', help='Plugin name.',
              metavar='NAME', required=True)
@click.option('--path', '-p', help='Host directory.',
              metavar='PATH', required=True)
@click.option('--create', '-c', help='Create on the fly.', is_flag=True)
@click.option('--user-only', '-u', help='Just for current user.', is_flag=True)
def main(name: str, path: str, create: bool, user_only: bool) -> None:
    """Script's main entry point."""
    if create:
        __create_on_the_fly(name, path)
    # Try to load the module to verify the configuration
    module = None
    try:
        module = load_module(name, path)
    except PypeError as ex:
        print_error(f'Could not find a python module "{name}" at {path}: {ex}')
        exit(1)
    # Check __init__.py
    init_file = join(path, name, '__init__.py')
    if not isfile(init_file):
        print_error(f'Could not find __init__.py at {init_file}. '
                    + 'This plugin path seems invalid.')
        exit(1)
    # Append plugin to global configuration
    config_handler = PypeConfigHandler()
    config = config_handler.get_config()
    if any([plugin for plugin in config.plugins
            if plugin.name == name]):
        print_error(f'There is already a plugin named "{name}".')
        exit(1)
    path = __replace_parentfolder_if_relative_to_config(
        path, config_handler.get_file_path())
    path = __replace_homefolder_with_tilde(path)
    users = [getpass.getuser()] if user_only else []
    config.plugins.append(ConfigurationPlugin(module.__name__, path, users))
    config_handler.set_config(config)

    print_success(f'Plugin "{name}" successfully registered.')


def __replace_homefolder_with_tilde(plugin_path: str) -> str:
    home_folder = resolve_path('~')
    return sub(home_folder, '~', plugin_path, flags=IGNORECASE)


def __replace_parentfolder_if_relative_to_config(
    plugin_path: str,
    config_path: str
) -> str:
    plugin_path_abs = resolve_path(plugin_path)
    config_dir_abs = resolve_path(dirname(config_path))
    return sub(sub(r'[/]+$', '', config_dir_abs, flags=IGNORECASE),
               '.', plugin_path_abs, flags=IGNORECASE)


def __create_on_the_fly(name: str, path: str) -> None:
    abspath = resolve_path(path)
    if not isdir(abspath):
        print_error(f'Path {abspath} does not point to a directoy.')
        exit(1)
    plugin_dir = join(abspath, name)
    if isdir(plugin_dir):
        print_error(f'Path {abspath} already exists.')
        exit(1)
    plugin_init_file = join(plugin_dir, '__init__.py')
    mkdir(plugin_dir)
    with open(plugin_init_file, 'w+') as init:
        init.write('"""' + NOT_DOCUMENTED_YET + '"""\n')
    print_success(f'Plugin "{name}" successfully created at {abspath}')
