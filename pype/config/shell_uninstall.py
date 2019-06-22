# -*- coding: utf-8 -*-
"""Uninstall pype's autocompletion and aliases."""

import click

from pype.core import PypeCore
from pype.util.cli import print_success


@click.command('shell_uninstall', help=__doc__)
def main():
    """Script's main entry point."""
    core = PypeCore()
    core.uninstall_from_shell()
    print_success('Done. Please source your rc-file or open a new shell.')
