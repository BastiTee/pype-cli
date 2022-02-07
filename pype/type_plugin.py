# -*- coding: utf-8 -*-
"""Data structure defining a plugin, i.e., a set of pypes."""

import getpass
import importlib
from glob import glob
from os import path
from sys import path as syspath
from typing import Any

from pype.config_model import ConfigurationPlugin
from pype.constants import NOT_DOCUMENTED_YET
from pype.errors import PypeError
from pype.type_pype import Pype
from pype.util.benchmark import Benchmark
from pype.util.iotools import resolve_path


class Plugin:
    """Data structure defining a plugin, i.e., a set of pypes."""

    def __init__(
        self,
        plugin: ConfigurationPlugin,
        config_path: str
    ) -> None:
        """Activate plugins for the provided configuration."""
        with Benchmark(plugin.name):
            self.__init_internal(plugin, config_path)

    def __init_internal(
        self,
        plugin: ConfigurationPlugin,
        config_path: str
    ) -> None:
        self.active = False
        if not self.__valid_for_user(plugin):
            return
        if plugin.path != '%INTERNAL%':
            # plugin pype
            self.name = plugin.name
            self.internal = False
            python_abspath = path.join(resolve_path(
                self.__handle_relative_path(
                    plugin.path,
                    config_path
                )))
            syspath.append(python_abspath)
            self.abspath = path.join(python_abspath, plugin.name)
        else:
            # internal pype
            self.name = 'pype.' + plugin.name
            self.internal = True
            self.abspath = path.join(path.dirname(
                __file__), plugin.name)
        try:
            self.module = importlib.import_module(self.name)
        # This used to be a ModuleNotFoundException but it's only Python >= 3.6
        except Exception:  # noqa: F821
            raise PypeError(
                f'No plugin named "{self.name}" found at {self.abspath}')
        self.doc = self.__get_docu_or_default(self.module)
        subfiles = [
            path.basename(file)
            for file in glob(self.abspath + '/*.py')
        ]
        subfiles = [file for file in subfiles
                    if not file.startswith('__')]
        self.pypes = [
            Pype(path.join(self.abspath, subfile), subfile, self.name)
            for subfile in subfiles
        ]
        self.active = True

    @staticmethod
    def __handle_relative_path(plugin_path: str, config_path: str) -> str:
        if not plugin_path.startswith('.'):
            return plugin_path
        return resolve_path(path.join(
            path.dirname(config_path),
            plugin_path
        ))

    @staticmethod
    def __get_docu_or_default(module: Any) -> str:
        return (
            module.__doc__ if module.__doc__ else NOT_DOCUMENTED_YET
        )

    @staticmethod
    def __valid_for_user(plugin: ConfigurationPlugin) -> bool:
        if not plugin.users or len(plugin.users) == 0:
            return True
        username = getpass.getuser()
        if any([user for user in plugin.users if user == username]):
            return True
        return False
