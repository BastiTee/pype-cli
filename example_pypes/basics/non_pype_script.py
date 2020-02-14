# -*- coding: utf-8 -*-
"""Script interoperable with pype-cli omitting any pype-cli libraries."""

# Import the "Command Line Interface Creation Kit"
# <https://click.palletsprojects.com>
import click

# Create a click command https://click.palletsprojects.com/en/7.x/commands/
# Notice that instead of using pype.fname_to_name(__file__) we just
# hard-wired the command name.
@click.command(name='non-pype-script', help=__doc__)
def main():
    """Script's main entry point."""
    print('I am a pype-cli independent script!')


if __name__ == '__main__':
    main()
