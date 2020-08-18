# -*- coding: utf-8 -*-
"""I/O utilities."""

from os import environ, path
from subprocess import PIPE, call, run
from time import time

from pype.constants import ENV_BENCHMARK_INIT
from pype.util.cli import print_benchmark, print_error


def run_interactive(cmdline, dry_run=False, verbose=False, *args, **kwargs):
    """Call an interactive shell."""
    if dry_run or verbose:
        print('$: {}'.format(cmdline))
    if dry_run:
        return
    try:
        return call(cmdline, shell=True, *args, **kwargs)
    except KeyboardInterrupt:
        pass


def run_and_get_output(cmdline, dry_run=False, verbose=False, *args, **kwargs):
    """Call a non-interactive shell and return stdout and stderr."""
    if dry_run or verbose:
        print('$: {}'.format(cmdline))
    if dry_run:
        return '', ''
    proc = run(cmdline, shell=True, stdout=PIPE, stderr=PIPE, *args, **kwargs)
    return proc.stdout.decode('utf-8'), proc.stderr.decode('utf-8')


def open_with_default(filepath):
    """Open the given filepath with the OS'es default application."""
    try:
        # Use open command
        run(['open', filepath], check=True)
    except Exception:
        # If not possible try to find $EDITOR or $VISUAL environment var
        editor = environ.get('EDITOR', None)
        if not editor:
            editor = environ.get('VISUAL', None)
        if not editor:
            print_error(
                'Open with default editor is not supported on this OS.')
            exit(1)
        run_interactive([editor, filepath])


def resolve_path(relative_path):
    """Resolve path including home folder expanding."""
    return path.abspath(path.expanduser(relative_path))


def benchmark_print_elapsed(key, start_time):
    """Print elapsed time since previous timestamp in milliseconds."""
    if int(environ.get(ENV_BENCHMARK_INIT, 0)) == 1:
        elapsed_ms = round((time() - start_time) * 1000, 5)
        print_benchmark('{} | {} ms'.format(key, elapsed_ms))


def benchmark_print_info(info_text):
    """Print a benchmark information text."""
    print_benchmark('– ' + info_text)
