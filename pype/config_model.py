# -*- coding: utf-8 -*-
"""Pype configuration types."""

from dataclasses import asdict as dc_asdict
from dataclasses import dataclass, field
from enum import Enum
from json import dumps
from typing import Any, List, Optional


class ConfigResolverSource(str, Enum):
    """Source of the resolved configuration file."""

    FROM_ENV = 1
    FROM_DEFAULT_PATH = 2
    FROM_SCRATCH_TO_DEFAULT_PATH = 3
    FROM_SCRATCH_TO_PROVIDED_PATH = 4


class BaseDataClass:
    """Base data class with asdict capability."""

    def asdict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return dc_asdict(self)  # type: ignore
        # https://github.com/python/mypy/issues/17550

    def asjson(self) -> str:
        """Convert to JSON."""
        return dumps(self.asdict(), indent=4)


@dataclass
class ConfigurationPlugin(BaseDataClass):
    """Configuration type for a single plugin."""

    name: str
    path: str
    users: List[str] = field(default_factory=list)


@dataclass
class ConfigurationAlias(BaseDataClass):
    """Configuration type for an alias."""

    alias: str
    command: str


@dataclass
class ConfigurationCoreLogging(BaseDataClass):
    """Core Configuration type for logging subsystem."""

    enabled: bool = False
    level: str = 'INFO'
    pattern: str = r'%(asctime)s %(levelname)s %(name)s %(message)s'
    directory: str = ''


@dataclass
class ConfigurationCore(BaseDataClass):
    """Core Configuration type."""

    logging: Optional[ConfigurationCoreLogging] = None


@dataclass
class Configuration(BaseDataClass):
    """Configuration type."""

    plugins: List[ConfigurationPlugin] = field(default_factory=list)
    aliases: List[ConfigurationAlias] = field(default_factory=list)
    core_config: Optional[ConfigurationCore] = None
