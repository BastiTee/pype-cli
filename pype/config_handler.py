# -*- coding: utf-8 -*-
"""Pype configuration handler."""

from enum import Enum
from json import JSONDecodeError, dump, load
from os import environ, mkdir, path
from sys import stderr

from colorama import Fore, Style
from jsonschema import ValidationError, validate

from pype.constants import ENV_CONFIG_FOLDER
from pype.exceptions import PypeException
from pype.util.iotools import resolve_path


class ConfigResolverSource(Enum):
    """Source of the resolved configuration file."""

    FROM_ENV = 1
    FROM_DEFAULT_PATH = 2
    FROM_SCRATCH_TO_DEFAULT_PATH = 3
    FROM_SCRATCH_TO_PROVIDED_PATH = 4


DEFAULT_CONFIG = {
    'plugins': [],
    'aliases': [],
    'core_config': {}
}

DEFAULT_CORE_CONFIG_LOGGING = {
    'enabled': False,
    'level': 'INFO',
    'pattern': '%(asctime)s %(levelname)s %(name)s %(message)s',
    'directory': None
}

CONFIG_SCHEMA_PATH = path.join(path.dirname(__file__), 'config-schema.json')
CONFIG_SCHEMA = load(open(CONFIG_SCHEMA_PATH))


class PypeConfigHandler:
    """Pype configuration handler."""

    DEFAULT_CONFIG_FOLDER = resolve_path('~/.pype-cli')
    DEFAULT_CONFIG_FILE = 'config.json'

    def __init__(self, init=True):
        """Construct a default configuaration handler."""
        self.filepath = None
        self.config = None
        if init:
            self.resolve_config_file()

    def resolve_config_file(self):
        """Resolve the configuration using various options.

        Returns an enum that explains from where the configuration was
        resolved.
        """
        config_source = None
        default_config_file = path.join(
            self.DEFAULT_CONFIG_FOLDER,
            self.DEFAULT_CONFIG_FILE
        )
        try:
            # Priority 1: Environment variable
            env_config_folder = environ[ENV_CONFIG_FOLDER]
            if not path.isdir(env_config_folder):
                raise PypeException(
                    f'Provided configuration folder {env_config_folder} '
                    + 'does not exist!')
            self.filepath = path.join(
                env_config_folder, self.DEFAULT_CONFIG_FILE
            )
            config_source = ConfigResolverSource.FROM_ENV
        except KeyError:
            # Priority 2: ~/.pype-cli/config.json
            if path.isfile(default_config_file):
                self.filepath = default_config_file
                config_source = ConfigResolverSource.FROM_DEFAULT_PATH
        # Priority 3: Create template config from scratch if nothing was found
        if not self.filepath:
            if not path.isdir(self.DEFAULT_CONFIG_FOLDER):
                mkdir(self.DEFAULT_CONFIG_FOLDER)
            dump(DEFAULT_CONFIG, open(default_config_file, 'w+'), indent=4)
            self.filepath = default_config_file
            config_source = ConfigResolverSource.FROM_SCRATCH_TO_DEFAULT_PATH
        try:
            self.config = load(open(self.filepath, 'r'))
        except JSONDecodeError:
            raise PypeException('Provided configuration file not valid JSON.')
        except FileNotFoundError:
            # Priorty 4: File name provided but file does not exist
            dump(DEFAULT_CONFIG, open(self.filepath, 'w+'), indent=4)
            self.config = load(open(self.filepath, 'r'))
            config_source = ConfigResolverSource.FROM_SCRATCH_TO_PROVIDED_PATH
        self.validate_config(self.config)
        return config_source

    def get_json(self):
        """Get pype configuration as JSON object."""
        return self.config

    def set_json(self, config):
        """Validate, set and persist configuration from JSON object."""
        self.validate_config(config)
        self.config = config
        # always update config file as well
        dump(self.config, open(self.filepath, 'w+'), indent=4)

    def get_file_path(self):
        """Get absolute filepath to configuration JSON file."""
        return self.filepath

    def get_dir_path(self):
        """Get absolute filepath to configuration directory."""
        return path.dirname(self.filepath)

    def validate_config(self, config):
        """Validate given config file against schema definition."""
        try:
            validate(instance=config, schema=CONFIG_SCHEMA)
        except ValidationError as err:
            print(Fore.RED + str(err) + Style.RESET_ALL + '\n', file=stderr)
            raise PypeException(
                'Configuration file is not valid. See above for details '
                + f'and refer to the schema file at {CONFIG_SCHEMA_PATH}')
        return True

    def get_core_config_logging(self, return_default_if_empty=False):
        """Return current or default logging configuration."""
        core_config = self.get_json().get('core_config', None)
        default_config = DEFAULT_CORE_CONFIG_LOGGING
        # Set default logging directory to pypes config folder
        default_config['directory'] = path.dirname(self.filepath)
        if not core_config:
            return default_config if return_default_if_empty else None
        logging_config = core_config.get('logging', None)
        if not logging_config:
            return default_config if return_default_if_empty else None
        return logging_config

    def set_core_config_logging(self, logging_config):
        """Set logging configuration."""
        config_json = self.get_json()
        if not config_json.get('core_config', None):
            config_json['core_config'] = {}
        config_json['core_config']['logging'] = logging_config
        self.set_json(config_json)  # Setter takes care of validation


def get_supported_log_levels():
    """Return supported log levels to be used with pype."""
    return (sorted(CONFIG_SCHEMA
                   ['properties']['core_config']['properties']['logging']
                   ['properties']['level']['enum']))
