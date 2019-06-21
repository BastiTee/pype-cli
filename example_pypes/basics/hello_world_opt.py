# -*- coding: utf-8 -*-
"""A classic hello world console feedback with click cli-options."""

import click


@click.command('hello_world_opt', help=__doc__)
@click.option('--message', '-m', default='Hello World!',
              help='Alternative message')
def cli(message):
    """Script's main entry point."""
    print(message)
