# -*- coding: utf-8 -*-
"""Install pype's autocompletion and aliases to a supported shell."""

import click

from pype.pype_core import PypeCore
from pype.util.iotools import resolve_path


@click.command(help=__doc__)
@click.option('--target-file', '-t', help='Target RC-file', required=True)
@click.option('--reverse', '-r', help='Uninstall autocompletion', is_flag=True)
def main(target_file, reverse):
    """Script's main entry point."""
    pype_core = PypeCore()
    shell_config = pype_core.get_shell_config()
    shell_config['target_file'] = resolve_path(target_file)
    if reverse:
        pype_core.uninstall_from_shell(shell_config)
    else:
        pype_core.install_to_shell(shell_config)
    print('Done. Please reload shell session.')


if __name__ == '__main__':
    main()
