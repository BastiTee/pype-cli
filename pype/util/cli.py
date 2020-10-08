# -*- coding: utf-8 -*-
"""CLI-functions for better user experience and consistency."""

from os import sep
from re import sub

import click


def fname_to_name(fname):
    """Use the filename as command name.

    You can omit calling this if you make sure to use dashes instead of
    underscores in your command name, e.g., hello-world instead of hello_world.
    This function just makes sure of that so you don't have to press shift to
    resolve it during execution.
    """
    return sub('_', '-', fname[:-3].split(sep)[-1])


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
    prefix = prefix + ' ' if prefix else ''
    click.echo(click.style(prefix + message.strip(), fg=color, bold=True))
