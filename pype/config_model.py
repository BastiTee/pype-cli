# -*- coding: utf-8 -*-
"""Pype configuration types."""

from dataclasses import asdict as dc_asdict
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class ConfigResolverSource(Enum):
    """Source of the resolved configuration file."""

    FROM_ENV = 1
    FROM_DEFAULT_PATH = 2
    FROM_SCRATCH_TO_DEFAULT_PATH = 3
    FROM_SCRATCH_TO_PROVIDED_PATH = 4


@dataclass
class ConfigurationPlugin:
    """Configuration type for a single plugin."""

    name: str
    path: str
    users: List[str] = field(default_factory=list)


@dataclass
class ConfigurationAlias:
    """Configuration type for an alias."""

    alias: str
    command: str


class ConfigurationCoreLoggingLevel(Enum):
    """Logging levels."""

    FATAL = 1
    ERROR = 2
    WARN = 3
    INFO = 4
    DEBUG = 5


@dataclass
class ConfigurationCoreLogging:
    """Core Configuration type for logging subsystem."""

    enabled: bool = False
    level: ConfigurationCoreLoggingLevel = ConfigurationCoreLoggingLevel.INFO
    pattern: str = r'%(asctime)s %(levelname)s %(name)s %(message)s'
    directory: str = ''


@dataclass
class ConfigurationCore:
    """Core Configuration type."""

    logging: Optional[ConfigurationCoreLogging] = None


@dataclass
class Configuration:
    """Configuration type."""

    plugins: List[ConfigurationPlugin] = field(default_factory=list)
    aliases: List[ConfigurationAlias] = field(default_factory=list)
    core_config: Optional[ConfigurationCore] = None

    def asdict(self) -> dict:
        """Convert to dictionary."""
        return dc_asdict(self)
