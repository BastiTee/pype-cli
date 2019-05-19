# -*- coding: utf-8 -*-

import subprocess
from os import environ, path
from sys import executable
from re import sub
from sys import path as syspath
from shutil import copyfile

import click

from pype.pype_core import PypeCore
from pype.util.iotools import open_with_default

# Load configuration file
try:
    CONFIG_FILE_PATH = environ['PYPE_CONFIG_JSON']
except KeyError:
    CONFIG_FILE_PATH = path.join(
        path.dirname(path.dirname(__file__)), 'config.json')

PYPE_CORE = PypeCore(CONFIG_FILE_PATH)
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
@click.pass_context
def main(ctx, list_pypes, open_pype):
    if list_pypes:
        PYPE_CORE.list_pypes()
        return
    global OPEN_PYPE
    OPEN_PYPE = open_pype
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())


def create_pype_from_template(pype_name, plugin):
    if plugin.internal:
        print('Creating internal pypes is not supported.')
        return
    target_name = sub('-', '_', sub(r'\.py$', '', pype_name))
    target_name = path.join(plugin.abspath, target_name + '.py')
    source_name = path.join(path.dirname(__file__), 'pype_template.py')
    if path.isfile(target_name):
        print('Pype already present')
        return
    copyfile(source_name, target_name)
    print('Created new pype', target_name)


def bind_plugin(name, plugin):
    @click.option('--create-pype', '-c',
                  help='Create new pype with provided name')
    @click.pass_context
    def plugin_binding_function(ctx, create_pype):
        if (create_pype):
            create_pype_from_template(create_pype, plugin)
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
