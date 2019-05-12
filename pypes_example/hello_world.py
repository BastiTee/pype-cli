#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A classic hello world console feedback."""

from argparse import ArgumentParser

DEFAULT_MESSAGE = 'Hello World!'

parser = ArgumentParser(description=__doc__)
parser.add_argument(
    '-m',
    metavar="MESSAGE",
    type=str,
    help='Optional message (defaults to \'{}\''.format(DEFAULT_MESSAGE))
parser.add_argument('pype', nargs='*')
args = parser.parse_args()

message = args.m if args.m else DEFAULT_MESSAGE
print(message)
