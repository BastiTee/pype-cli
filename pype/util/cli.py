# -*- coding: utf-8 -*-
"""CLI-functions for better user experience and consistency."""

import click

from pype.util import misc


def _create_short_names_for_commands(commands):
    short_names = misc.remove_common_prefix_from_string_list(
        misc.remove_common_suffix_from_string_list(
            [command['name'] for command in commands]
        ))
    for i in range(0, len(commands)):
        commands[i]['short_name'] = short_names[i]


def _get_command(name, commands, strip):
    selector = 'short_name' if strip else 'name'
    for command in commands:
        if command[selector] == name:
            return command


def generate_dynamic_multicommand(
        commands, callback_function, create_short_names=False):
    """Use provided dict to create a dynamic click.MultiCommand."""
    has_short_names = False
    if create_short_names:
        _create_short_names_for_commands(commands)
        has_short_names = True
    if len(commands) == len(
            [c for c in commands if c.get('short_name', None)]):
        has_short_names = True

    class DynamicCLI(click.MultiCommand):

        def list_commands(self, ctx):
            selector = 'short_name' if has_short_names else 'name'
            return [command[selector] for command in commands]

        def get_command(self, ctx, name):
            command = _get_command(name, commands, has_short_names)
            if not command:
                print_error('Command \'{}\' not found.'.format(name))
                exit(1)

            @click.command(name, help=command.get('help', None))
            @click.pass_context
            def invoke_callback(ctx):
                callback_function(command['name'], ctx)
            return invoke_callback
    return DynamicCLI


def ask_yes_or_no(question, default='yes'):
    """Ask user a yes/no question and return their answer."""
    valid = {'yes': True, 'y': True, 'ye': True,
             'no': False, 'n': False}
    if default is None:
        prompt = ' [y/n] '
    elif default == 'yes':
        prompt = ' [Y/n] '
    elif default == 'no':
        prompt = ' [y/N] '
    else:
        raise ValueError('invalid default answer: {}'.format(default))

    while True:
        print(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print('Please respond with "yes" or "no" (or "y" or "n").')


def ask_for_text(question):
    """Ask user for free text input and return their answer."""
    print(question)
    return input('> ')


def print_success(message):
    """Print a message with a green success highlight."""
    _print_highlight(message, '✔', 'green')


def print_warning(message):
    """Print a message with a yellow warning highlight."""
    _print_highlight(message, '⚠', 'yellow')


def print_error(message):
    """Print a message with a red error highlight."""
    _print_highlight(message, '✘', 'red')


def _print_highlight(message, prefix, color):
    click.echo(click.style(prefix + ' ' + message.strip(),
                           fg=color, bold=True))
