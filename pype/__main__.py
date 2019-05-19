# -*- coding: utf-8 -*-

import subprocess
from os import environ, path, remove
from re import sub
from shutil import copyfile
from sys import executable
from sys import path as syspath

import click

from pype.pype_core import PypeCore
from pype.util.iotools import open_with_default

PYPE_CORE = PypeCore()
OPEN_PYPE = False
CREATE_PYPE = False


@click.group(
    invoke_without_command=True,
    context_settings=dict(help_option_names=['-h', '--help'])
)
@click.option('--list-pypes', '-l', is_flag=True,
              help='Print all available pypes')
@click.option('--open-pype', '-o', is_flag=True,
              help='Open selected pype in default editor')
@click.option('--open-config', '-c', is_flag=True,
              help='Open config file in default editor')
@click.pass_context
def main(ctx, list_pypes, open_pype, open_config):
    if open_config:
        open_with_default(PYPE_CORE.get_config_filepath())
        return
    if list_pypes:
        PYPE_CORE.list_pypes()
        return

    global OPEN_PYPE
    OPEN_PYPE = open_pype
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())


def bind_plugin(name, plugin):
    @click.option('--create-pype', '-c',
                  help='Create new pype with provided name')
    @click.option('--delete-pype', '-d',
                  help='Deletes pype for provided name')
    @click.pass_context
    def plugin_binding_function(ctx, create_pype, delete_pype):
        if (create_pype):
            PYPE_CORE.create_pype_from_template(create_pype, plugin)
        elif (delete_pype):
            PYPE_CORE.delete_pype_by_name(delete_pype, plugin)
    plugin_binding_function.__name__ = name
    return plugin_binding_function


def bind_pype(name, plugin, pype):
    @click.pass_context
    @click.argument('extra_args', nargs=-1, type=click.UNPROCESSED)
    @click.option('--help', '-h', is_flag=True)
    def pype_binding_function(ctx, extra_args, help):
        if (OPEN_PYPE):
            # If '-o' option was selected to open pype in default editor
            if plugin.internal:
                print('WARNING: Editing internal pypes can break stuff.')
            open_with_default(pype.abspath)
            return
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
        invoke_without_command=True)(plugin_binding_function)
    ctx_settings = dict(
        ignore_unknown_options=True,
        allow_extra_args=True
    )
    for pype in plugin.pypes:
        plugin_click_group.command(context_settings=ctx_settings)(
            bind_pype(pype.name, plugin, pype))
