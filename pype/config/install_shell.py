# -*- coding: utf-8 -*-
"""Install pype's autocompletion and aliases to a supported shell."""

from os import path, remove
from pype.util.iotools import resolve_path
from pype.util.misc import get_from_json_or_default
from pype.pype_core import get_configuration

import click

SHELL_INIT_PREFIX = '.pype-initfile'
SUPPORTED_SHELLS = {
    'bash': {
        'init_file': path.join(path.expanduser('~'),
                               SHELL_INIT_PREFIX + '-bash'),
        'source_cmd': 'eval "$(_PYPE_COMPLETE=source pype)"'
    },
    'zsh': {
        'init_file': path.join(path.expanduser('~'),
                               SHELL_INIT_PREFIX + '-zsh'),
        'source_cmd': 'eval "$(_PYPE_COMPLETE=source_zsh pype)"'
    }
}


@click.command()
@click.option('--shell', '-s',
              help='Shell {}'.format(SUPPORTED_SHELLS),
              required=True)
@click.option('--target-file', '-t',
              help='Target RC-file',
              required=True)
@click.option('--reverse', '-r',
              help='Uninstall autocompletion',
              is_flag=True)
def main(shell, target_file, reverse):

    if not any(
        [supported for supported in SUPPORTED_SHELLS
         if shell == supported]
    ):
        print('Unsupported shell \'{}\'.'.format(shell))
        return
    shell_config = SUPPORTED_SHELLS[shell]
    shell_config['target_file'] = resolve_path(target_file)
    if reverse:
        uninstall(shell_config)
    else:
        install(shell_config)
    print('Done. Please reload shell session.')


def install(shell_config):
    aliases = get_from_json_or_default(get_configuration(), 'aliases', [])
    print('Writing init-file', shell_config['init_file'])
    print('Found aliases:', aliases)
    with open(shell_config['init_file'], 'w+') as ifile:
        # Write pype sourcing command
        ifile.write('if [ ! -z "$( command -v pype )" ]; then\n')
        ifile.write('\t' + shell_config['source_cmd'] + '\n')
        # Write configured aliases
        for alias in aliases:
            alias_cmd = '\talias {}="{}"\n'.format(
                alias['alias'], alias['command'])
            ifile.write(alias_cmd)
        ifile.write('fi\n')
    # Only add source link to target file if not present yet
    try:
        rc_file_content = open(shell_config['target_file'], 'r').readlines()
    except FileNotFoundError:
        rc_file_content = []
    already_present = [line for line in rc_file_content
                       if SHELL_INIT_PREFIX in line]
    if not already_present:
        print('Adding init-file sourcing to', shell_config['target_file'])
        with open(shell_config['target_file'], 'a+') as rc_file_handle:
            rc_file_handle.write('. ' + shell_config['init_file'] + '\n')


def uninstall(shell_config):
    if path.isfile(shell_config['init_file']):
        remove(shell_config['init_file'])
    if not path.isfile(shell_config['target_file']):
        return
    with open(shell_config['target_file'], 'r') as f:
        lines = f.readlines()
    with open(shell_config['target_file'], 'w') as f:
        for line in lines:
            if SHELL_INIT_PREFIX not in line.strip('\n'):
                f.write(line)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
