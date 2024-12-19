# -*- coding: utf-8 -*-
"""$ pype <plugin> --create-pype/--delete-pype."""

import importlib
from typing import Generator

import pytest

from pype.config import plugin_register, plugin_unregister
from tests import RunnerEnvironment, create_runner, create_test_env

test_run: RunnerEnvironment


class TestCLIPypePypes:  # noqa: D101

    plugin = 'test-plugin'

    @pytest.fixture(autouse=True, scope='module')
    def _run_around_tests(self) -> Generator:
        with create_test_env() as test_env:
            # Before all
            global test_run
            test_run = create_runner(
                test_env,
                plugin_register.main,
                ['--name', self.plugin, '--path', '%CONFIG_DIR%', '--create'])
            assert test_run.result.exit_code == 0
            assert 'successfully created' in test_run.result.output

            # Run test
            yield

            # After all
            # Reload to activate current test_env
            importlib.reload(plugin_unregister)
            result = test_run.runner.invoke(
                plugin_unregister.main,
                ['--name', self.plugin])
            assert result.exit_code == 0
            assert 'successfully unregistered' in result.output

    def test_registered_plugin_found(self) -> None:  # noqa: D102
        global test_run
        result = test_run.runner.invoke(
            test_run.reload_and_get_main
        )
        assert result.exit_code == 0
        assert self.plugin in result.output

    def test_plugin_called_without_options(self) -> None:  # noqa: D102
        global test_run
        result = test_run.runner.invoke(
            test_run.reload_and_get_main, [
                self.plugin
            ]
        )
        assert result.exit_code == 0
        assert 'Usage: main test-plugin' in result.output

    def test_delete_non_existing_pype(self) -> None:  # noqa: D102
        global test_run
        result = test_run.runner.invoke(
            test_run.reload_and_get_main, [
                self.plugin, '--delete-pype', 'nan'
            ]
        )
        assert result.exit_code == 2
        assert 'Invalid value for \'--delete-pype\'' in result.output

    def test_create_pype(self) -> None:  # noqa: D102
        global test_run
        result = test_run.runner.invoke(
            test_run.reload_and_get_main, [
                self.plugin, '--create-pype', 'test'
            ]
        )
        assert result.exit_code == 0
        assert 'Created new pype' in result.output
