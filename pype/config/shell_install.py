# -*- coding: utf-8 -*-
"""Install pype's autocompletion and aliases."""

import click

from pype.core import PypeCore
from pype.util.cli import print_success


@click.command('shell_install', help=__doc__)
def cli():
    """Script's main entry point."""
    core = PypeCore()
    core.install_to_shell()
    print_success('Done. Please source your rc-file or open a new shell.')
