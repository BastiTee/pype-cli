# -*- coding: utf-8 -*-
"""I/O utilities."""

from os import path, listdir
from re import match, IGNORECASE
from subprocess import run, call


def run_interactive(cmdline, *args, **kwargs):
    """Calls to an interactive shell."""
    if not isinstance(cmdline, str):
        cmdline = ' '.join(cmdline)
    try:
        call(cmdline, shell=True, *args, **kwargs)
    except KeyboardInterrupt:
        pass


def run_and_get_output(cmdline, *args, **kwargs):
    """Runs a cmdline non-interactive and returns both stderr and stdout."""
    proc = run(cmdline, capture_output=True, **kwargs)
    return proc.stdout.decode('utf-8'), proc.stderr.decode('utf-8')


def open_with_default(filepath):
    """Opens the given filepath with the OS'es default editor."""
    try:
        run(['open', filepath], check=True)
    except FileNotFoundError:
        print('Open with default editor is not supported on this OS.')


def resolve_path(relative_path):
    """Resolve path including home folder expanding."""
    return path.abspath(path.expanduser(relative_path))


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
