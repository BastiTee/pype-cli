# -*- coding: utf-8 -*-
"""A classic hello world console feedback with click cli-options."""

# Import the "Command Line Interface Creation Kit"
# <https://click.palletsprojects.com>
import click

import pype

# Create a click command https://click.palletsprojects.com/en/7.x/commands/


@click.command(name=pype.fname_to_name(__file__), help=__doc__)
# Add an option https://click.palletsprojects.com/en/7.x/options/
@click.option('--message', '-m', default='Hello World!',
              metavar='MESSAGE', help='Alternative message')
def main(message: str) -> None:
    """Script's main entry point."""
    print(message)
