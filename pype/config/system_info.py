# -*- coding: utf-8 -*-
"""Print system information."""

import platform
import sys
from os import environ

import click
from tabulate import tabulate

from pype.config_handler import PypeConfigHandler
from pype.constants import ENV_CONFIG_FOLDER
from pype.core import in_virtualenv
from pype.util.cli import fname_to_name


@click.command(name=fname_to_name(__file__), help=__doc__)
def main():
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
        ['EFFECTIVE CONFIG FILE', PypeConfigHandler(init=True).filepath]
    )
    infos.append(
        ['IN VIRTUAL ENV', in_virtualenv()]
    )
    print(tabulate(infos))
