# -*- coding: utf-8 -*-
"""I/O utilities."""

from os import path, listdir
from re import match, IGNORECASE


def get_immediate_subfiles(file_path, pattern=None, ignorecase=False):
    """Return the sub-files of a given file path, but only the first level."""

    if not file_path:
        raise TypeError('file_path not provided.')

    files = []
    for name in listdir(file_path):
        if path.isdir(path.join(file_path, name)):
            continue
        if pattern:
            if ignorecase and match(pattern, name, IGNORECASE):
                files.append(name)
            elif match(pattern, name):
                files.append(name)
            continue
        files.append(name)
    files.sort()
    return files
