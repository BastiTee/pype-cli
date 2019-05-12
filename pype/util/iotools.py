#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import os
import re


def get_immediate_subfiles(file_path, pattern=None, ignorecase=False):
    """Return the sub-files of a given file path, but only the first level."""

    if not file_path:
        raise TypeError('file_path not provided.')

    files = []
    for name in os.listdir(file_path):
        if os.path.isdir(os.path.join(file_path, name)):
            continue
        if pattern:
            if ignorecase and re.match(pattern, name, re.IGNORECASE):
                files.append(name)
            elif re.match(pattern, name):
                files.append(name)
            continue
        files.append(name)
    files.sort()
    return files
