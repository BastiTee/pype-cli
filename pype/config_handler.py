# -*- coding: utf-8 -*-
"""Pype configuration handler."""

from json import JSONDecodeError, dump, load
from os import environ, mkdir, path
from sys import stderr
from typing import List

from colorama import Fore, Style
from dacite import from_dict
from jsonschema import ValidationError, validate

from pype import config_model
from pype.config_model import (ConfigResolverSource, Configuration,
                               ConfigurationCore, ConfigurationCoreLogging)
from pype.constants import ENV_CONFIG_FOLDER
from pype.errors import PypeError
from pype.util.iotools import resolve_path

DEFAULT_CONFIG = config_model.Configuration(
    plugins=[],
    aliases=[],
    core_config=config_model.ConfigurationCore()
)

DEFAULT_CONFIG_DICT: dict = DEFAULT_CONFIG.asdict()


CONFIG_SCHEMA_PATH = path.join(path.dirname(__file__), 'config-schema.json')
CONFIG_SCHEMA = load(open(CONFIG_SCHEMA_PATH))


class PypeConfigHandler:
    """Pype configuration handler."""

    def __init__(
        self,
        default_config_folder: str = resolve_path('~/.pype-cli'),
        default_config_filename: str = 'config.json'
    ) -> None:
        """Construct a default configuaration handler."""
        default_config_file = path.join(
            default_config_folder,
            default_config_filename
        )
        try:
            # Priority 1: Environment variable
            env_config_folder = environ[ENV_CONFIG_FOLDER]
            if not path.isdir(env_config_folder):
                raise PypeError(
                    f'Provided configuration folder {env_config_folder} '
                    + 'does not exist!')
            self.filepath = path.join(
                env_config_folder, default_config_filename
            )
            self.config_source = ConfigResolverSource.FROM_ENV
        except KeyError:
            # Priority 2: ~/.pype-cli/config.json
            if path.isfile(default_config_file):
                self.filepath = default_config_file
                self.config_source = ConfigResolverSource.FROM_DEFAULT_PATH
            else:
                self.filepath = ''
        # Priority 3: Create template config from scratch if nothing was found
        if not self.filepath:
            if not path.isdir(default_config_folder):
                mkdir(default_config_folder)
            dump(DEFAULT_CONFIG_DICT, open(default_config_file, 'w+'),
                 indent=4)
            self.filepath = default_config_file
            self.config_source = (
                ConfigResolverSource.FROM_SCRATCH_TO_DEFAULT_PATH
            )
        try:
            self.config_json = load(open(self.filepath, 'r'))
        except JSONDecodeError:
            raise PypeError('Provided configuration file not valid JSON.')
        except FileNotFoundError:
            # Priorty 4: File name provided but file does not exist
            dump(DEFAULT_CONFIG_DICT, open(self.filepath, 'w+'), indent=4)
            self.config_json = load(open(self.filepath, 'r'))
            self.config_source = (
                ConfigResolverSource.FROM_SCRATCH_TO_PROVIDED_PATH
            )
        self.validate_config(self.config_json)
        self.config = from_dict(Configuration, self.config_json)

    def get_config(self) -> Configuration:
        """Get pype configuration."""
        return self.config

    def set_config(self, config: Configuration) -> None:
        """Validate, set and persist configuration."""
        self.validate_config(config.asdict())
        self.config_json = config.asdict()
        # always update config file as well
        dump(self.config_json, open(self.filepath, 'w+'), indent=4)

    def get_file_path(self) -> str:
        """Get absolute filepath to configuration JSON file."""
        return self.filepath

    def get_dir_path(self) -> str:
        """Get absolute filepath to configuration directory."""
        return path.dirname(self.filepath)

    def get_config_source(self) -> ConfigResolverSource:
        """Return indicator from which config was resolved."""
        return self.config_source

    def get_core_config_logging(self) -> ConfigurationCoreLogging:
        """Return current or default logging configuration."""
        core_config = self.get_config().core_config
        default_config = config_model.ConfigurationCoreLogging()
        default_config.directory = path.dirname(self.filepath)
        if not core_config or not core_config.logging:
            return default_config
        return core_config.logging

    def set_core_config_logging(
        self,
        logging_config: ConfigurationCoreLogging
    ) -> None:
        """Set logging configuration."""
        config = self.get_config()
        if not config.core_config:
            config.core_config = ConfigurationCore()
        config.core_config.logging = logging_config
        self.set_config(config)  # Setter takes care of validation

    @staticmethod
    def validate_config(config: dict) -> bool:
        """Validate given config file against schema definition."""
        try:
            validate(instance=config, schema=CONFIG_SCHEMA)
        except ValidationError as err:
            print(Fore.RED + str(err) + Style.RESET_ALL + '\n', file=stderr)
            raise PypeError(
                'Configuration file is not valid. See above for details '
                + f'and refer to the schema file at {CONFIG_SCHEMA_PATH}')
        return True


def get_supported_log_levels() -> List[str]:
    """Return supported log levels to be used with pype."""
    return (sorted(CONFIG_SCHEMA
                   ['properties']['core_config']['properties']['logging']
                   ['properties']['level']['enum']))
