# -*- coding: utf-8 -*-
"""Utility functions."""

import json
import sys
from pygments import highlight
from pygments.lexers.data import JsonLexer
from pygments.formatters.terminal import TerminalFormatter


def get_from_json_or_default(json, path, default_value):
    if not path:
        return default_value
    json = json if json else {}
    try:
        for breadcrumb in path.split('.'):
            json = json[breadcrumb]
        return json if json else default_value
    except KeyError:
        return default_value


def beautify_json_string(json_string, colorize=False, sort_keys=False):
    json_obj = json.loads(json_string)
    formatted_json = json.dumps(json_obj, sort_keys=sort_keys, indent=4)
    if not colorize:
        return formatted_json
    return highlight(formatted_json, JsonLexer(), TerminalFormatter())


def get_key_or_none(object, key):
    try:
        return object[key]
    except KeyError:
        return None


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
