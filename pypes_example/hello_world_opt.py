#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A classic hello world console feedback with an option."""

import click
DEFAULT_MESSAGE = 'Hello World!'


@click.command()
def main():
    print('hello')

# parser = ArgumentParser(description=__doc__)
# parser.add_argument(
#     '-m',
#     metavar="MESSAGE",
#     type=str,
#     help='Optional message (defaults to \'{}\''.format(DEFAULT_MESSAGE))
# parser.add_argument('pype', nargs='*')
# args = parser.parse_args()

# message = args.m if args.m else DEFAULT_MESSAGE


if __name__ == "__main__":
    main()
