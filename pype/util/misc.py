# -*- coding: utf-8 -*-

"""Utility functions."""

import logging


def get_or_default(json, path, default_value):
    try:
        for breadcrumb in path.split('.'):
            json = json[breadcrumb]
        return json if json else default_value
    except KeyError:
        logging.getLogger(__name__).error(
            'Invalid config key \'{}\''.format(path))
        return default_value


def get_kwarg_value_or_empty(kwargs, key):
    if not kwargs or not key:
        raise ValueError('Input kwargs or key must be set.')
    try:
        value = kwargs[key]
        return str(value).strip() if value else ''
    except KeyError:
        return ''
