#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Pype

:copyright: (c) 2019 by Basti Tee.
:license: Apache 2.0, see LICENSE for more details.
"""

from argparse import ArgumentParser
from pype_core import PypeCore

if __name__ == "__main__":
    parser = ArgumentParser(description="pype")
    parser.add_argument(
        '-c',
        metavar="CONFIG_JSON",
        type=str,
        help='Pype configuration file (defaults to config.json)')
    parser.add_argument(
        '-v',
        action='store_true',
        help='Set logging to DEBUG')
    parser.add_argument('pype_command', nargs='*')
    PypeCore(parser.parse_args())
