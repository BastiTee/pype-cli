#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""PYPE - A command-line tool for command-line tools."""

from os import listdir, path
from re import sub
from sys import path as syspath
from typing import Any, Callable, List

import click
from click import Choice
from colorama import init

from pype.core import PypeCore, print_context_help
from pype.errors import PypeError
from pype.type_plugin import Plugin
from pype.util.benchmark import Benchmark
from pype.util.cli import fname_to_name, print_error
from pype.util.iotools import open_with_default

PYPE_CORE = PypeCore()


@click.group(
    invoke_without_command=True,
    context_settings=dict(help_option_names=['-h', '--help']),
    help=__doc__
)
@click.option(
    '--list-pypes', '-l', is_flag=True,
    help='Print all available pypes.'
)
@click.option(
    '--aliases', '-a', is_flag=True,
    help='Print all available aliases.'
)
@click.option(
    '--alias-register', '-r', metavar='ALIAS',
    help='Register alias for following pype.'
)
@click.option(
    '--alias-unregister', '-u', metavar='ALIAS',
    type=click.Choice(PYPE_CORE.get_aliases()), help='Unregister alias.'
)
@click.option(
    '--open-config', '-o', is_flag=True,
    help='Open config file in default editor.'
)
@click.pass_context
def main(
    ctx: Any,
    list_pypes: bool,
    aliases: bool,
    open_config: bool,
    alias_register: str,
    alias_unregister: str
) -> None:
    """Pype main entry point."""
    if not _process_alias_configuration(
            ctx, list_pypes, open_config, alias_register, alias_unregister):
        print_context_help(ctx, level=1)
        return
    if open_config:
        PYPE_CORE.open_config_with_default()
    elif list_pypes:
        PYPE_CORE.list_pypes()
        return
    elif aliases:
        PYPE_CORE.print_aliases()
        return
    elif alias_unregister:
        PYPE_CORE.alias_unregister(alias_unregister)
        return
    elif ctx.invoked_subcommand is None:
        print_error('No pype selected.')
        print_context_help(ctx, level=1)


def _bind_plugin(
    plugin_name: str,
    plugin: Plugin
) -> Callable:

    class PypeCLI(click.MultiCommand):

        def __init__(self, **attrs: Any) -> None:
            click.MultiCommand.__init__(
                self,
                invoke_without_command=True,
                **attrs)

        def list_commands(self, ctx: Any) -> List:
            Benchmark.print_info(f'Loading pypes from plugin {plugin_name}')
            rv = []
            for filename in listdir(plugin.abspath):
                if filename.endswith('.py') and '__' not in filename:
                    rv.append(fname_to_name(filename))
            rv.sort()
            return rv

        def get_command(self, ctx: click.Context, name: str) -> Any:
            name = sub('-', '_', name)
            full_name = plugin.name + '.' + name
            try:
                with Benchmark(key=full_name):
                    syspath.append(path.dirname(plugin.abspath))
                    mod = __import__(full_name, {}, {}, ['main'])
                    return mod.main
            except ImportError as import_error:
                print_error(str(import_error))
                exit(1)

        @staticmethod
        def get_pype_command_names(plugin: Plugin) -> List[str]:
            return [sub('_', '-', pype.name) for pype in plugin.pypes]

    @click.option(
        '--create-pype', '-c', metavar='PYPE',
        help='Create new pype with given name.'
    )
    @click.option(
        '--open-pype', '-o', metavar='PYPE',
        help='Open pype with given name in default editor.',
        type=Choice(PypeCLI.get_pype_command_names(plugin))
    )
    @click.option(
        '--delete-pype', '-d', metavar='PYPE',
        help='Delete pype with given name.',
        type=Choice(PypeCLI.get_pype_command_names(plugin))
    )
    @click.option(
        '--minimal', '-m', is_flag=True,
        help='Use a minimal template with less boilerplate '
        + '(only used along with "--create-pype" option).'
    )
    @click.option(
        '--edit', '-e', is_flag=True,
                  help='Open new pype immediately for editing '
                  + '(only used along with "--create-pype" option).'
    )
    @click.pass_context
    def _plugin_bind_plugin_function(
            ctx: Any,
            create_pype: str,
            minimal: bool,
            edit: bool,
            delete_pype: str,
            open_pype: str
    ) -> None:
        if (minimal or edit) and not create_pype:
            print_error(
                '"-m" and "-e" can only be used with "-c" option.')
            print_context_help(ctx, level=2)
            return
        toggle_invoked = False
        created_pype_abspath = None
        if create_pype:  # Handle creation of pypes
            created_pype_abspath = PYPE_CORE.create_pype_or_exit(
                create_pype, plugin, minimal)
            toggle_invoked = True
        if delete_pype:  # Handle deletion of pypes
            PYPE_CORE.delete_pype(delete_pype, plugin)
            toggle_invoked = True
        if open_pype or edit:  # Handle opening existing or new pypes
            if plugin.internal:
                print_error('Opening internal pypes is not supported.')
                return
            # Resolve either an existing or a newly created pype
            pype_abspath = (PYPE_CORE.get_abspath_to_pype(
                plugin, sub('-', '_', open_pype))
                if open_pype else created_pype_abspath)
            if not pype_abspath:
                print_error(f'Pype "{open_pype}" could not be found.')
                return
            open_with_default(pype_abspath)
            toggle_invoked = True
        if ctx.parent.alias_register:
            PYPE_CORE.alias_register(ctx)
            exit(0)
        # Handle case that no toggles were used and no commands selected
        if not toggle_invoked and not ctx.invoked_subcommand:
            print_context_help(ctx, level=2)
    _plugin_bind_plugin_function.__name__ = plugin_name
    main.command(cls=PypeCLI,
                 help=plugin.doc)(_plugin_bind_plugin_function)
    return _plugin_bind_plugin_function


def _process_alias_configuration(
        ctx: Any,
        list_pypes: bool,
        open_config: bool,
        alias_register: str,
        alias_unregister: str
) -> bool:
    if alias_register and alias_unregister:
        print_error('Options -r and -u cannot be combined.')
        return False
    other_options = open_config or list_pypes
    if alias_register and other_options:
        print_error('Option -r cannot be combined with other options.')
        return False
    if alias_unregister and other_options:
        print_error('Option -u cannot be combined with other options.')
        return False
    # piggy-back context
    ctx.alias_register = alias_register
    return True


init(autoreset=True)  # Initialize colorama
try:
    [
        _bind_plugin(plugin.name, plugin)
        for plugin in PYPE_CORE.get_plugins()
    ]
except PypeError as pype_error:
    print_error(str(pype_error))
    exit(1)
