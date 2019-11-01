# -*- coding: utf-8 -*-
"""A classic hello world console feedback with click cli-options."""

# Import the "Command Line Interface Creation Kit"
import click

# You can omit this if you make sure to use dashes instead of underscores in
# your command name, e.g., hello-world instead of hello_world.
# This function just makes sure of that so you don't have to press shift to
# resolve it during execution.
from pype.core import fname_to_name

# Create a click command https://click.palletsprojects.com/en/7.x/commands/
@click.command(name=fname_to_name(__file__), help=__doc__)
# Add an option https://click.palletsprojects.com/en/7.x/options/
@click.option('--message', '-m', default='Hello World!',
              metavar='MESSAGE', help='Alternative message')
def main(message):
    """Script's main entry point."""
    print(message)
