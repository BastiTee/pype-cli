# -*- coding: utf-8 -*-
"""$ pype pype-config plugin-register/plugin-unregister."""

import importlib

from pype.config import plugin_register, plugin_unregister
from tests import create_runner, create_test_env, invoke_runner, reload_config


class TestCLIPypePluginRegister:  # noqa: D101

    def test_register_without_name(self) -> None:  # noqa: D102
        test_run = invoke_runner(plugin_register.main)
        assert test_run.result.exit_code == 2
        assert 'Missing option \'--name\'' in test_run.result.output

    def test_register_without_path(self) -> None:  # noqa: D102
        test_run = invoke_runner(
            plugin_register.main, ['--name', 'test'])
        assert test_run.result.exit_code == 2
        assert 'Missing option \'--path\'' in test_run.result.output

    def test_register_without_create(self) -> None:  # noqa: D102
        test_run = invoke_runner(
            plugin_register.main,
            ['--name', 'plug', '--path', '%CONFIG_DIR%'])
        assert test_run.result.exit_code == 1
        assert 'Could not find a python module' in test_run.result.output

    def test_register_with_create(self) -> None:  # noqa: D102
        test_run = invoke_runner(
            plugin_register.main,
            ['--name', 'plug', '--path', '%CONFIG_DIR%', '--create'])
        assert test_run.result.exit_code == 0
        assert 'successfully created' in test_run.result.output

    def test_register_twice(self) -> None:  # noqa: D102
        with create_test_env() as test_env:
            # Register plugin
            test_run = create_runner(
                test_env,
                plugin_register.main,
                ['--name', 'plug', '--path', '%CONFIG_DIR%', '--create'])
            assert test_run.result.exit_code == 0
            assert 'successfully created' in test_run.result.output
            result_configuration = reload_config(test_run)
            assert len(result_configuration['plugins']) == 1
            assert result_configuration['plugins'][0]['name'] == 'plug'
            # Try to register again
            result = test_run.runner.invoke(
                plugin_register.main,
                ['--name', 'plug', '--path', test_run.test_env.config_dir])
            assert result.exit_code == 1
            assert 'already a plugin named' in result.output
            assert len(result_configuration['plugins']) == 1

    def test_register_unregister_and_reregister(self) -> None:  # noqa: D102
        with create_test_env() as test_env:
            # Register plugin
            test_run = create_runner(
                test_env,
                plugin_register.main,
                ['--name', 'plug', '--path', '%CONFIG_DIR%', '--create'])
            assert test_run.result.exit_code == 0
            assert 'successfully created' in test_run.result.output
            result_configuration = reload_config(test_run)
            assert len(result_configuration['plugins']) == 1
            assert result_configuration['plugins'][0]['name'] == 'plug'

            # Unregister plugin (doesn't delete)
            # Reload to activate current test_env
            importlib.reload(plugin_unregister)
            result = test_run.runner.invoke(
                plugin_unregister.main,
                ['--name', 'plug'])
            assert result.exit_code == 0
            assert 'successfully unregistered' in result.output
            result_configuration = reload_config(test_run)
            assert len(result_configuration['plugins']) == 0

            # Register plugin again
            result = test_run.runner.invoke(
                plugin_register.main,
                ['--name', 'plug', '--path', test_env.config_dir])
            assert result.exit_code == 0
            assert 'successfully registered' in result.output
            result_configuration = reload_config(test_run)
            assert len(result_configuration['plugins']) == 1
            assert result_configuration['plugins'][0]['name'] == 'plug'
