# -*- coding: utf-8 -*-
"""Register a new pype plugin."""


import click

from pype.pype_core import load_module, PypeCore
from pype.pype_exception import PypeException


@click.command()
@click.option('--name', '-n', help='Plugin module name', required=True)
@click.option('--path', '-p', help='Module directory', required=True)
def main(name, path):
    # Try to load the module to verify the configuration
    try:
        module = load_module(name, path)
    except PypeException:
        print('Could not find a python module \'{}\' at {}'
              .format(name, path))
        exit(1)
    pype_core = PypeCore()
    pype_core.resolve_config_file()
    config_json = pype_core.get_config_json()
    config_json['plugins'].append({
        'name': module.__name__,
        'path': path
    })
    pype_core.set_config_json(config_json)
    print('Plugin \'{}\' successfully registered.'.format(name))


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
