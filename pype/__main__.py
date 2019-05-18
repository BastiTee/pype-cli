# -*- coding: utf-8 -*-

import subprocess
from os import environ, path
from sys import executable
from sys import path as syspath

import click

from pype.pype_core import PypeCore

"""
eval "$(_PYPE_COMPLETE=source pype)"

"""

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    # ignore_unknown_options=True,
    # allow_extra_args=True,
)
CONFIG_FILE_PATH = path.join(
    path.dirname(path.dirname(__file__)), 'config.json')
PYPE_CORE = PypeCore(CONFIG_FILE_PATH)


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option('--verbose', '-v', is_flag=True, help='Show verbose output')
@click.option('--list-pypes', '-l', is_flag=True, help='Print available pypes')
@click.pass_context
def main(ctx, verbose, list_pypes):
    PYPE_CORE.configure_logging(verbose)
    if list_pypes:
        PYPE_CORE.list_pypes()
        return
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())


def bind_plugin(name, plugin):
    @click.pass_context
    def plugin_binding_function(ctx):
        pass
    plugin_binding_function.__name__ = name
    return plugin_binding_function


def bind_pype(name, plugin, pype):
    @click.pass_context
    @click.argument('extra_args', nargs=-1, type=click.UNPROCESSED)
    @click.option('--help', '-h', is_flag=True)
    def pype_binding_function(ctx, extra_args, help):
        syspath.append(path.dirname(plugin.abspath))
        sub_environment = environ.copy()
        sub_environment['PYTHONPATH'] = ':'.join(syspath)
        extra_args = ['--help'] if help else list(ctx.params['extra_args'])
        command = [executable, '-m', plugin.name +
                   '.' + pype.name] + extra_args
        subprocess.run(command, env=sub_environment)
    pype_binding_function.__name__ = name
    return pype_binding_function


for plugin in PYPE_CORE.get_plugins():
    plugin_binding_function = bind_plugin(plugin.name, plugin)
    plugin_click_group = main.group(
        invoke_without_command=False)(plugin_binding_function)
    ctx_settings = dict(
        ignore_unknown_options=True,
        allow_extra_args=True
    )
    for pype in plugin.pypes:
        plugin_click_group.command(context_settings=ctx_settings)(
            bind_pype(pype.name, plugin, pype))
