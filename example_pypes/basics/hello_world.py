# -*- coding: utf-8 -*-
"""A classic hello world console feedback."""

import click

from pype.core import fname_to_name


@click.command(name=fname_to_name(__file__), help=__doc__)
def main():
    """Script's main entry point."""
    print('Hello World!')
