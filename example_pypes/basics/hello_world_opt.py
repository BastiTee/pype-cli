# -*- coding: utf-8 -*-
"""A classic hello world console feedback with click cli-options."""

import click


@click.command(help=__doc__)
@click.option('--message', '-m', default='Hello World!',
              help='Alternative message')
def main(message):
    print(message)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
