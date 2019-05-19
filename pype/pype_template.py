# -*- coding: utf-8 -*-
"""Not documented yet."""

# Pype's go-to library to create command-line interfaces.
# Visit <https://click.palletsprojects.com> for details.
import click

# Decorator to initialize a CLI-command with options
@click.command()
# A typical option that requires another argument, e.g., a string option
@click.option('--option', '-o', default='default', help='An option')
# A typical toggle-option
@click.option('--verbose', '-v', is_flag=True, help='A toggle')
def main(option, verbose):
    print('- option:', option)
    print('- verbose:', verbose)

    # Your code goes here ...


if __name__ == "__main__":  # Only invoke main if called directly
    main()  # pylint: disable=no-value-for-parameter
