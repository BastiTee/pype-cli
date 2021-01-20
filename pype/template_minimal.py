# -*- coding: utf-8 -*-
"""Not documented yet."""

import click

import pype


@click.command(name=pype.fname_to_name(__file__), help=__doc__)
def main() -> None:  # noqa: D103
    pass
