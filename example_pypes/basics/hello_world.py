# -*- coding: utf-8 -*-
"""A classic hello world console feedback."""

# Import the "Command Line Interface Creation Kit"
# <https://click.palletsprojects.com>
import click

import pype

# Create a click command https://click.palletsprojects.com/en/7.x/commands/


@click.command(name=pype.fname_to_name(__file__), help=__doc__)
def main() -> None:
    """Script's main entry point."""
    print('Hello World!')
