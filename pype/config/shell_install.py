# -*- coding: utf-8 -*-
"""Install pype's autocompletion and aliases."""

from os.path import basename
from sys import argv

import click

from pype.core import PypeCore, fname_to_name
from pype.util.cli import print_success


@click.command(name=fname_to_name(__file__), help=__doc__)
def main():
    """Script's main entry point."""
    shell_command = basename(argv[0])
    core = PypeCore()
    core.install_to_shell(shell_command)
    print_success('Done. Please source your rc-file or open a new shell.')
