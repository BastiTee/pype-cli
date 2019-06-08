# -*- coding: utf-8 -*-
"""Uninstall pype's autocompletion and aliases."""

import click

from colorama import Fore, init

from pype.core import PypeCore


@click.command(help=__doc__)
def main():
    """Script's main entry point."""
    core = PypeCore()
    core.uninstall_from_shell()
    print(Fore.RED + 'Done. Please source your rc-file or open a new shell.')


if __name__ == '__main__':
    init(autoreset=True)
    main()
