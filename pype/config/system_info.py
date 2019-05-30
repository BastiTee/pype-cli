# -*- coding: utf-8 -*-
"""Print system information useful for bug reports or other inspections."""

import platform

import click


@click.command(help=__doc__)
def main():
    """Script's main entry point."""
    print("""-- PYPE SYSTEM ENVIRONMENT
MACHINE:   {}
PROCESSOR: {}
PLATFORM:  {}
VERSION:   {}
RELEASE:   {}
SYSTEM:    {}
""".format(
        platform.machine(),
        platform.processor(),
        platform.platform(),
        platform.version(),
        platform.release(),
        platform.system()
    ))


if __name__ == '__main__':
    main()
