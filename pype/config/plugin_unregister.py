# -*- coding: utf-8 -*-
"""Unregister an existing plugin."""


import click

from pype.config_handler import PypeConfigHandler
from pype.util.cli import fname_to_name, print_success, print_warning


@click.command(name=fname_to_name(__file__), help=__doc__)
@click.option('--name', '-n', help='Plugin name.',
              metavar='NAME', required=True)
def main(name):
    """Script's main entry point."""
    # Try to load the module to verify the configuration
    config_handler = PypeConfigHandler()
    config_json = config_handler.get_json()
    new_plugins = [
        plugin for plugin in config_json['plugins']
        if plugin['name'] != name
    ]
    if config_json['plugins'] == new_plugins:
        print_warning('Plugin "{}" not found. Nothing to do.'.format(name))
        return
    config_json['plugins'] = new_plugins
    config_handler.set_json(config_json)
    print_success('Plugin "{}" successfully unregistered.'.format(name))
