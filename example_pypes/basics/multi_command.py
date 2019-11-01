# -*- coding: utf-8 -*-
"""A dynamic multi-command creator.

This pype demonstrating how to utilize the multi command processor
bundled with pype-cli.
"""

import json

# Import the "Command Line Interface Creation Kit"
# <https://click.palletsprojects.com>
import click

import pype

# Place to store your dynamic commands
commands_registry = pype.resolve_path('~/.pype-example-multicommands')


def _load_command_registry():
    """Load the available commands from a json file."""
    try:
        commands = json.load(open(commands_registry, 'r'))
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        commands = []  # Fallback on first initialization
    return commands


def _generate_multi_command():
    """Create the subcommand registry."""
    commands = _load_command_registry()
    return [{
        'name': command,
        'help': 'Execute ' + command
    } for command in commands]


def _command_callback(command, context):
    """Process the passed subcommand."""
    print('Executing ' + command)
    print('Command context: ' + str(context))


# Create a new click command with dynamic sub commands
@click.command(
    name=pype.fname_to_name(__file__), help=__doc__,
    # This will allow to call the pype without a sub command
    invoke_without_command=True,
    # Initialize dynamic subcommands using the convenience function
    cls=pype.generate_dynamic_multicommand(
        # Add a function to create multi commands, in this case
        # based on the existing command registry.
        _generate_multi_command(),
        # Provide a callback to receive the command and the
        # click context object.
        _command_callback
    )
)
# Add an option to extend the command registry
@click.option('--add', '-a', metavar='COMMAND_NAME',
              help='Add a new subcommand')
# Pass the context to be able to print the help text
@click.pass_context
def main(ctx, add):
    """Script's main entry point."""
    # Load the current registry from a local json-file
    command_registry = _load_command_registry()
    # If add option was selected...
    if add:
        if add in command_registry:
            print(add + ' already registered.')
            exit(0)
        click.confirm(
            'Add ' + add + ' to commands?', default=False, abort=True)
        # Register and save the new command
        command_registry.append(add)
        json.dump(command_registry, open(commands_registry, 'w+'))
    # ... else just print the help text.
    elif ctx.invoked_subcommand is None:
        print(ctx.get_help())
