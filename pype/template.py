# -*- coding: utf-8 -*-
"""Not documented yet."""

# Import the "Command Line Interface Creation Kit"
# <https://click.palletsprojects.com>
import click

# For colored output pype includes the colorama library
from colorama import Fore, Style

# You can omit this if you make sure to use dashes instead of underscores in
# your command name, e.g., hello-world instead of hello_world.
# This function just makes sure of that so you don't have to press shift to
# resolve it during execution.
from pype.core import fname_to_name
# Import some utilities that are bundled with pype-cli
from pype.util import cli
from pype.util.iotools import run_interactive


# Create a click command https://click.palletsprojects.com/en/7.x/commands/
@click.command(name=fname_to_name(__file__), help=__doc__)
# Add options https://click.palletsprojects.com/en/7.x/options/
@click.option('--option', '-o', default='default', help='An option')
@click.option('--verbose', '-v', is_flag=True, help='A toggle')
def main(option, verbose):
    """Script's main entry point."""
    # Print out something in shiny colors
    cli.print_success('Yay!')
    cli.print_warning('Meh.')
    cli.print_error('Oh no!')

    # Use colorama directly
    print(Fore.RED + '- option:  ' + Style.DIM + Fore.GREEN + option)
    print(Fore.RED + '- verbose: ' + Style.DIM + Fore.GREEN + str(verbose))

    # Use a pype utility
    run_interactive('ls')

    # Your code goes here ...
