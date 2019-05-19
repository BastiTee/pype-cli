# -*- coding: utf-8 -*-
"""Not documented yet"""


import click


@click.command()
@click.option('--option', '-o', default='default', help='An option')
@click.option('--verbose', '-v', is_flag=True, help='A toggle')
def main(option, verbose):
    print('Option:', option)
    print('Verbose:', verbose)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
