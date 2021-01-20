# -*- coding: utf-8 -*-
"""Print system information."""

import platform
import sys
from os import environ
from typing import Iterable, cast

import click
import pkg_resources
from tabulate import tabulate

from pype.config_handler import PypeConfigHandler
from pype.constants import ENV_CONFIG_FOLDER
from pype.core import get_pype_basepath, in_virtualenv
from pype.util.cli import fname_to_name


@click.command(name=fname_to_name(__file__), help=__doc__)
def main() -> None:
    """Script's main entry point."""
    unset = 'Not set'
    print('PYPE SYSTEM ENVIRONMENT')
    # System
    infos = [
        ['MACHINE', platform.machine()],
        ['PROCESSOR', platform.processor()],
        ['PLATFORM', platform.platform()], ['VERSION', platform.version()],
        ['RELEASE', platform.release()], ['SYSTEM', platform.system()],
        ['PY VERSION', sys.version.replace('\n', '')], [
            'PY VERSION_INFO', sys.version_info],
        ['SHELL', environ.get('SHELL', unset)]
    ]
    # Relevant environment infos
    env_config_folder_set = ENV_CONFIG_FOLDER in environ.keys()
    infos.append(['$' + ENV_CONFIG_FOLDER + ' SET', env_config_folder_set])
    env_keys = [key for key in environ.keys() if 'pype_' in key.lower()]
    for env_key in env_keys:
        infos.append(
            [env_key, environ[env_key]]
        )
    # Effective configuration
    infos.append(
        ['EFFECTIVE CONFIG FILE', PypeConfigHandler().filepath]
    )
    infos.append(['IN VIRTUAL ENV', in_virtualenv()])
    # Version info
    base_path = get_pype_basepath()
    version = pkg_resources.get_distribution('pype-cli').version
    infos.append(['PYPE-CLI VERSION', version])
    infos.append(['PYPE-CLI INSTALL', base_path])
    # Output
    print(tabulate(cast(Iterable[Iterable[str]], infos)))
