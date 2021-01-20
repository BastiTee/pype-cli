# -*- coding: utf-8 -*-
"""I/O utilities."""

from os import environ, path
from subprocess import PIPE, call, run
from typing import List, Tuple

from pype.util.cli import print_error


def run_interactive(
        cmdline: List[str],
        dry_run: bool = False,
        verbose: bool = False,
        *args: str,
        **kwargs: int
) -> int:
    """Call an interactive shell."""
    if dry_run or verbose:
        print(f'$: {cmdline}')
    if dry_run:
        return 0
    try:
        return call(cmdline, shell=True,  # type: ignore  # noqa
            *args, **kwargs)  # type: ignore  # noqa
    except KeyboardInterrupt:
        return 0


def run_and_get_output(
    cmdline: List[str],
    dry_run: bool = False,
    verbose: bool = False,
    *args: str,
    **kwargs: int
) -> Tuple[str, str]:
    """Call a non-interactive shell and return stdout and stderr."""
    if dry_run or verbose:
        print(f'$: {cmdline}')
    if dry_run:
        return '', ''
    proc = run(cmdline, shell=True, stdout=PIPE,  # type: ignore  # noqa
               stderr=PIPE, *args, **kwargs)
    return proc.stdout.decode('utf-8'), proc.stderr.decode('utf-8')


def open_with_default(filepath: str) -> None:
    """Open the given filepath with the OS'es default application."""
    try:
        # Use open command
        run(['open', filepath], check=True)
    except Exception:  # noqa: B902
        # If not possible try to find $EDITOR or $VISUAL environment var
        editor = environ.get('EDITOR', None)
        if not editor:
            editor = environ.get('VISUAL', None)
        if not editor:
            print_error(
                'Open with default editor is not supported on this OS.')
            exit(1)
        run_interactive([editor, filepath])


def resolve_path(relative_path: str) -> str:
    """Resolve path including home folder expanding."""
    return path.abspath(path.expanduser(relative_path))
