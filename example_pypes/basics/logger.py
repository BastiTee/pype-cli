# -*- coding: utf-8 -*-
"""How to use the global logging subsystem."""

import logging

import click

import pype


@click.command(name=pype.fname_to_name(__file__), help=__doc__)
def main() -> None:
    """Script's main entry point."""
    # For this to work it is required that you've set up global logging
    # via 'pype pype.config logger' before. See its help pages to get yourself
    # familiar with the options.

    # Name your logger. Note that this can be omitted but you will end up
    # with the default 'root' logger.
    logger = logging.getLogger(__name__)

    # Log something to the global log file. Note that the output to the file
    # depends on the logging configuration mentioned above.
    logger.debug('Debug message')
    logger.info('Info message')
