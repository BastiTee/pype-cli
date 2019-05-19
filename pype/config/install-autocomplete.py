# -*- coding: utf-8 -*-
"""Install bash/zsh autocompletion for pype."""

from os import path

import click


@click.command()
@click.option('--shell', '-s', help='Shell (bash or zsh)', required=True)
def main(shell):
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
            rc_file_handle.write('\n# pype-cli auto-complete initialization\n')
            rc_file_handle.write('. ' + init_file + '\n')
        changed = True
    print('Configure script: {}'.format(init_file))
    if changed:
        print('Done. Please reload shell session to apply auto-completion.')
    else:
        print('Already configured.')


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
