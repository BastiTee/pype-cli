# -*- coding: utf-8 -*-
"""Install pype's autocompletion and aliases."""

import click

from pype.core import PypeCore, fname_to_name
from pype.util.cli import print_success


@click.command(name=fname_to_name(__file__), help=__doc__)
@click.option('--one-tab', '-o', is_flag=True,
              help='Auto-complete on single press of TAB-key')
def main(one_tab):
    """Script's main entry point."""
    core = PypeCore()
    core.install_to_shell(one_tab=one_tab)
    print_success('Done. Please source your rc-file or open a new shell.')
