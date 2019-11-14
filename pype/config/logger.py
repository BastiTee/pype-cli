# -*- coding: utf-8 -*-
"""Configure global logging."""

import contextlib
from json import dumps

import click

from pype.config_handler import PypeConfigHandler, get_supported_log_levels
from pype.util.cli import fname_to_name, print_error, print_success


@contextlib.contextmanager
def open_configuration():
    """Open configuration file context."""
    cfg_handler = PypeConfigHandler()
    log_cfg = cfg_handler.get_core_config_logging(return_default_if_empty=True)
    yield log_cfg
    cfg_handler.set_core_config_logging(log_cfg)


@click.group(name=fname_to_name(__file__), help=__doc__)
def main():  # noqa: D103
    pass


@main.command(help='Configure log level')
@click.argument('level', metavar='LOGLEVEL', nargs=1,
                type=click.Choice(get_supported_log_levels()))
def set_level(level):  # noqa: D103
    with open_configuration() as log_cfg:
        log_cfg['level'] = level
    print_success('Log level set to {}.'.format(level))


@main.command(help='Configure log pattern')
@click.argument('pattern', metavar='LOGPATTERN', nargs=1)
def set_pattern(pattern):  # noqa: D103, A002
    if not pattern or len(pattern) == 0:
        print_error('Logging pattern cannot be empty.')
        exit(1)
    pattern = pattern.strip()
    with open_configuration() as log_cfg:
        log_cfg['pattern'] = pattern
    print_success('Log pattern set to \'{}\'.'.format(pattern))


@main.command(help='Configure target directory')
@click.argument('directory', metavar='TARGETDIR', nargs=1,
                type=click.Path(exists=True, writable=True))
def set_directory(directory):  # noqa: D103
    with open_configuration() as log_cfg:
        log_cfg['directory'] = directory
    print_success('Log directory set to \'{}\'.'.format(directory))


@main.command(help='Enable global logger')
def enable():  # noqa: D103
    with open_configuration() as log_cfg:
        log_cfg['enabled'] = True
    print_success('Global logging enabled.')


@main.command(help='Disable global logger')
def disable():  # noqa: D103
    with open_configuration() as log_cfg:
        log_cfg['enabled'] = False
    print_success('Global logging disabled.')


@main.command(help='Print current configuration')
def print_config():  # noqa: D103
    with open_configuration() as log_cfg:
        print(dumps(log_cfg, indent=4))
