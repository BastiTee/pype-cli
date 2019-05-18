# -*- coding: utf-8 -*-
"""Utility functions."""


def get_or_default(json, path, default_value):
    if not path:
        return default_value
    json = json if json else {}
    try:
        for breadcrumb in path.split('.'):
            json = json[breadcrumb]
        return json if json else default_value
    except KeyError:
        return default_value
