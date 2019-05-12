#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Pype: A Python framework for your command-line tooling needs"""

from pype.pype_core import PypeCore
import click

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--verbose', '-v', is_flag=True,
              help='Show verbose output')
@click.option('--list-pypes', '-l', is_flag=True,
              help='Print available pypes')
@click.option('--config', '-c', default='config.json',
              help='Pype configuration file')
@click.argument('pype', nargs=-1, type=click.UNPROCESSED)
def main(config, verbose, list_pypes, pype):
    PypeCore(config, verbose, list_pypes, pype)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
