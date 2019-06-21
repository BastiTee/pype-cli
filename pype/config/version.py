# -*- coding: utf-8 -*-
"""Print current pype version."""

import click

import pkg_resources

from pype.core import get_pype_basepath


@click.command('version', help=__doc__)
def cli():
    """Script's main entry point."""
    base_path = get_pype_basepath()
    version = pkg_resources.get_distribution('pype-cli').version
    print('{} @ {}'.format(version, base_path))
