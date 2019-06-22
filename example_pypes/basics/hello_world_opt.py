# -*- coding: utf-8 -*-
"""A classic hello world console feedback with click cli-options."""

import click

from pype.core import fname_to_name


@click.command(name=fname_to_name(__file__), help=__doc__)
@click.option('--message', '-m', default='Hello World!',
              help='Alternative message')
def main(message):
    """Script's main entry point."""
    print(message)
