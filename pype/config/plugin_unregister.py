# -*- coding: utf-8 -*-
"""Unregister an existing plugin."""


from typing import List

import click

from pype.config_handler import PypeConfigHandler
from pype.util.cli import fname_to_name, print_success, print_warning


def __resolve_available_plugins() -> List[str]:
    return [plugin['name']
            for plugin in PypeConfigHandler().get_json()['plugins']]


@click.command(name=fname_to_name(__file__), help=__doc__)
@click.option('--name', '-n', help='Plugin name.',
              type=click.Choice(__resolve_available_plugins()),
              metavar='NAME', required=True)
def main(name: str) -> None:
    """Script's main entry point."""
    # Try to load the module to verify the configuration
    config_handler = PypeConfigHandler()
    config_json = config_handler.get_json()
    new_plugins = [
        plugin for plugin in config_json['plugins']
        if plugin['name'] != name
    ]
    if config_json['plugins'] == new_plugins:
        print_warning(f'Plugin "{name}" not found. Nothing to do.')
        return
    config_json['plugins'] = new_plugins
    config_handler.set_json(config_json)
    print_success(f'Plugin "{name}" successfully unregistered.')
