# -*- coding: utf-8 -*-
"""Install bash/zsh autocompletion for pype."""

from os import path, remove

import click


@click.command()
@click.option('--shell', '-s', help='Shell (bash or zsh)', required=True)
@click.option('--reverse', '-r', help='Uninstall autocompletion', is_flag=True)
def main(shell, reverse):
    if not shell or ('bash' not in shell and 'zsh' not in shell):
        print('Unsupported shell \'{}\'.'.format(shell))
        return
    if 'bash' in shell:
        target_file = path.join(path.expanduser('~'), '.bashrc')
        init_file = path.join(path.expanduser('~'), '.pype-autcomplete-bash')
        command = 'eval "$(_PYPE_COMPLETE=source pype)"'
    elif 'zsh' in shell:
        target_file = path.join(path.expanduser('~'), '.zshrc')
        init_file = path.join(path.expanduser('~'), '.pype-autcomplete-zsh')
        command = 'eval "$(_PYPE_COMPLETE=source_zsh pype)"'
    if reverse:
        uninstall(init_file, target_file)
    else:
        install(init_file, target_file, command)


def install(init_file, target_file, command):
    changed = False
    if not path.isfile(init_file):
        print('Creating init-file', init_file)
        with open(init_file, 'w+') as ifile:
            ifile.write(command + '\n')
        changed = True
    # Only add source link if not present yet
    try:
        rc_file_content = open(target_file, 'r').readlines()
    except FileNotFoundError:
        rc_file_content = []
    pype_source = [line for line in rc_file_content
                   if '.pype-autcomplete' in line]
    if not pype_source:
        print('Adding init-file sourcing to', target_file)
        with open(target_file, 'a+') as rc_file_handle:
            rc_file_handle.write('. ' + init_file + '\n')
        changed = True
    print('Configure script: {}'.format(init_file))
    if changed:
        print('Done. Please reload shell session to apply auto-completion.')
    else:
        print('Already installed.')


def uninstall(init_file, target_file):
    changed = False
    if path.isfile(init_file):
        changed = True
        remove(init_file)
    if path.isfile(target_file):
        with open(target_file, 'r') as f:
            lines = f.readlines()
        with open(target_file, 'w') as f:
            for line in lines:
                if init_file not in line.strip('\n'):
                    f.write(line)
                else:
                    changed = True
    if changed:
        print('Done. Please reload shell session.')
    else:
        print('Already uninstalled.')


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
