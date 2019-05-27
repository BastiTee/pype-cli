# -*- coding: utf-8 -*-
"""Unregister an existing pype plugin."""


import click

from pype.pype_core import PypeCore


@click.command(help=__doc__)
@click.option('--name', '-n', help='Plugin module name', required=True)
def main(name):
    """Script's main entry point."""
    # Try to load the module to verify the configuration
    pype_core = PypeCore()
    config_json = pype_core.get_config_json()
    new_plugins = [
        plugin for plugin in config_json['plugins']
        if plugin['name'] != name
    ]
    if config_json['plugins'] == new_plugins:
        print('Plugin "{}" not found. Nothing to do.'.format(name))
        return
    config_json['plugins'] = new_plugins
    pype_core.set_config_json(config_json)
    print('Plugin "{}" successfully unregistered.'.format(name))


if __name__ == '__main__':
    main()
