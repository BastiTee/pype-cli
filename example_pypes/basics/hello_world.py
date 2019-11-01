# -*- coding: utf-8 -*-
"""A classic hello world console feedback."""

# Import the "Command Line Interface Creation Kit"
import click

# You can omit this if you make sure to use dashes instead of underscores in
# your command name, e.g., hello-world instead of hello_world.
# This function just makes sure of that so you don't have to press shift to
# resolve it during execution.
from pype.core import fname_to_name

# Create a click command https://click.palletsprojects.com/en/7.x/commands/
@click.command(name=fname_to_name(__file__), help=__doc__)
def main():
    """Script's main entry point."""
    print('Hello World!')
