# -*- coding: utf-8 -*-
"""pype.config_model."""

import json
from os.path import dirname, join

from pype import config_model


class TestPypeConfigModel:  # noqa: D101

    def test_init(self) -> None:  # noqa: D102
        config = config_model.Configuration()
        assert config.asdict() == {
            'plugins': [],
            'aliases': [],
            'core_config': None
        }

    def test_loggingconfig(self) -> None:  # noqa: D102
        config = config_model.Configuration()
        config.core_config = config_model.ConfigurationCore()
        config.core_config.logging = config_model.ConfigurationCoreLogging()
        logging_as_dict = config.core_config.logging.asdict()
        assert logging_as_dict == {
            'directory': '',
            'enabled': False,
            'level': 'INFO',
            'pattern':
            r'%(asctime)s %(levelname)s %(name)s %(message)s',
        }
        config_as_dict = config.asdict()
        assert config_as_dict == {
            'plugins': [],
            'aliases': [],
            'core_config': {
                'logging': logging_as_dict
            }
        }

    def test_aliasconfig(self) -> None:  # noqa: D102
        config = config_model.Configuration()
        config.aliases.append(config_model.ConfigurationAlias(
            'myalias', 'pype config'
        ))
        alias_as_dict = config.aliases[0].asdict()
        assert alias_as_dict == {
            'alias': 'myalias',
            'command': 'pype config'
        }
        config_as_dict = config.asdict()
        assert config_as_dict == {
            'plugins': [],
            'aliases': [
                alias_as_dict
            ],
            'core_config': None
        }

    def test_pluginconfig(self) -> None:  # noqa: D102
        config = config_model.Configuration()
        config.plugins.append(config_model.ConfigurationPlugin(
            'p1', '/somewhere', ['bastitee']
        ))
        plugin_as_dict = config.plugins[0].asdict()
        assert plugin_as_dict == {
            'name': 'p1',
            'path': '/somewhere',
            'users': [
                'bastitee'
            ]
        }
        config_as_dict = config.asdict()
        assert config_as_dict == {
            'plugins': [plugin_as_dict],
            'aliases': [],
            'core_config': None
        }

    def test_to_from_json(self) -> None:  # noqa: D102
        config = config_model.Configuration()
        config.plugins.append(config_model.ConfigurationPlugin(
            'p1', '/somewhere', ['bastitee']
        ))
        config.aliases.append(config_model.ConfigurationAlias(
            'myalias', 'pype config'
        ))
        config.core_config = config_model.ConfigurationCore()
        config.core_config.logging = config_model.ConfigurationCoreLogging()
        json_str_expected = json.dumps(json.load(
            open(join(dirname(__file__), 'test_config_model.json'))
        ), indent=4)
        assert config.asjson() == json_str_expected
