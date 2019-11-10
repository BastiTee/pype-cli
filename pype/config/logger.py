# -*- coding: utf-8 -*-
"""Configure global logging."""

import click

from pype.core import PypeCore
from pype.util.cli import fname_to_name


@click.command(name=fname_to_name(__file__), help=__doc__)
def main():
    """Script's main entry point."""
    core = PypeCore()
    core.install_to_shell()
