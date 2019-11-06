# -*- coding: utf-8 -*-
"""Pype configuration handler."""

from enum import Enum
from json import JSONDecodeError, dump, load
from os import environ
from os.path import dirname, isfile, join
from sys import stderr

from colorama import Fore, Style

from jsonschema import ValidationError, validate

from pype.constants import ENV_CONFIG_FILE
from pype.exceptions import PypeException
from pype.util.iotools import resolve_path


class ConfigResolverSource(Enum):
    """Source of the resolved configuration file."""

    FROM_TEST_SETUP = 0
    FROM_ENV = 1
    FROM_DEFAULT_PATH = 2
    FROM_RELATIVE_FILE = 3
    FROM_SCRATCH_TO_DEFAULT_PATH = 4
    FROM_SCRATCH_TO_PROVIDED_PATH = 5


DEFAULT_CONFIG = {
    'plugins': [],
    'aliases': [],
    'core_config': {}
}


class PypeConfigHandler:
    """Pype configuration handler."""

    DEFAULT_CONFIG_FILE = resolve_path('~/.pype-config.json')
    LOCAL_CONFIG_FILE = join(dirname(dirname(__file__)), 'config.json')
    CONFIG_SCHEMA_PATH = join(dirname(__file__), 'config-schema.json')
    CONFIG_SCHEMA = load(open(CONFIG_SCHEMA_PATH))

    def __init__(self, test_config_file=None):
        """Construct a default configuaration handler."""
        self.config = None
        self.filepath = None
        self.test_config_file = test_config_file

    def resolve_config_file(self):
        """Resolve the configuration using various options.

        Returns an enum that explains from where the configuration was
        resolved.
        """
        # Evaluate test bypass to ignore any environment configuration
        if self.test_config_file:
            self.filepath = self.test_config_file
            self.config = load(open(self.filepath, 'r'))
            return ConfigResolverSource.FROM_TEST_SETUP
        config_source = None
        try:
            # Priority 1: Environment variable
            self.filepath = environ[ENV_CONFIG_FILE]
            config_source = ConfigResolverSource.FROM_ENV
        except KeyError:
            # Priority 2: ~/.pype-config.json
            if isfile(self.DEFAULT_CONFIG_FILE):
                self.filepath = self.DEFAULT_CONFIG_FILE
                config_source = ConfigResolverSource.FROM_DEFAULT_PATH
            # Priority 3: ./config.json
            elif isfile(self.LOCAL_CONFIG_FILE):
                self.filepath = self.LOCAL_CONFIG_FILE
                config_source = ConfigResolverSource.FROM_RELATIVE_FILE
        # Priority 4: Create a template config from scratch if no path provided
        if not self.filepath:
            dump(DEFAULT_CONFIG, open(self.DEFAULT_CONFIG_FILE, 'w+'))
            self.filepath = self.DEFAULT_CONFIG_FILE
            config_source = ConfigResolverSource.FROM_SCRATCH_TO_DEFAULT_PATH
        try:
            self.config = load(open(self.filepath, 'r'))
        except JSONDecodeError:
            raise PypeException('Provided configuration file not valid JSON.')
        except (FileNotFoundError, JSONDecodeError):
            # Priorty 5: File name provided but file does not
            dump(DEFAULT_CONFIG, open(self.filepath, 'w+'))
            self.config = load(open(self.filepath, 'r'))
            config_source = ConfigResolverSource.FROM_SCRATCH_TO_PROVIDED_PATH
        self.validate_config(self.config)
        return config_source

    def get_json(self):
        """Get pype configuration as JSON object."""
        if not self.config:
            self.resolve_config_file()
        return self.config

    def get_filepath(self):
        """Get absolute filepath to configuration JSON file."""
        if not self.config:
            self.resolve_config_file()
        return self.filepath

    def set_json(self, config):
        """Validate, set and persist configuration from JSON object."""
        self.validate_config(config)
        self.config = config
        # always update config file as well
        dump(self.config, open(self.filepath, 'w+'), indent=4)

    def validate_config(self, config):
        """Validate given config file against schema definition."""
        try:
            validate(instance=config, schema=self.CONFIG_SCHEMA)
        except ValidationError as err:
            print(Fore.RED + str(err) + Style.RESET_ALL + '\n', file=stderr)
            raise PypeException(
                'Configuration file is not valid. See above for details '
                + 'and refer to the schema file at {}'.format(
                    self.CONFIG_SCHEMA_PATH))
        return True
