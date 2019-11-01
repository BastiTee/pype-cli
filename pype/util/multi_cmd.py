# -*- coding: utf-8 -*-
"""Dynamic multi command processing."""

import click

from pype.util.cli import print_error


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


def _create_short_names_for_commands(commands):
    """Strip common pre- and postfixes from command list."""
    short_names = _remove_common_prefix_from_string_list(
        _remove_common_postfix_from_string_list(
            [command['name'] for command in commands]
        ))
    for i in range(0, len(commands)):
        commands[i]['short_name'] = short_names[i]


def _remove_common_prefix_from_string_list(string_list):
    """If a list of strings share the same prefix they will be removed."""
    if any([len(string) < 2 or not string for string in string_list]):
        return string_list
    uniq_first_char = len(set([string[:1] for string in string_list]))
    if uniq_first_char == 1:
        string_list = _remove_common_prefix_from_string_list(
            [string[1:] for string in string_list])
    return string_list


def _remove_common_postfix_from_string_list(string_list):
    """If a list of strings share the same postfix they will be removed."""
    if any([len(string) < 2 or not string for string in string_list]):
        return string_list
    uniq_last_char = len(set([string[-1:] for string in string_list]))
    if uniq_last_char == 1:
        string_list = _remove_common_postfix_from_string_list(
            [string[:-1] for string in string_list])
    return string_list


def _get_command(name, commands, strip):
    """Pick a command from the list either by short name or name."""
    selector = 'short_name' if strip else 'name'
    for command in commands:
        if command[selector] == name:
            return command
