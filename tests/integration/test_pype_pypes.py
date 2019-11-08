# -*- coding: utf-8 -*-
"""$ pype <plugin> --create-pype/--delete-pype."""

from pype.config import plugin_register, plugin_unregister

import pytest

from tests import create_runner, create_test_env


class TestCLIPypePypes:  # noqa: D101

    plugin = 'test-plugin'

    @pytest.fixture(autouse=True, scope='module')
    def _run_around_tests(self):
        with create_test_env() as test_env:
            # Before all
            pytest.test_run = create_runner(
                test_env,
                plugin_register.main,
                ['--name', self.plugin, '--path', '%CONFIG_DIR%', '--create'])
            assert pytest.test_run.result.exit_code == 0
            assert 'successfully created' in pytest.test_run.result.output

            # Run test
            yield

            # After all
            result = pytest.test_run.runner.invoke(
                plugin_unregister.main,
                ['--name', self.plugin])
            assert result.exit_code == 0
            assert 'successfully unregistered' in result.output

    def test_registered_plugin_found(self):  # noqa: D102
        result = pytest.test_run.runner.invoke(
            pytest.test_run.main
        )
        assert result.exit_code == 0
        assert self.plugin in result.output

    def test_plugin_called_without_options(self):  # noqa: D102
        result = pytest.test_run.runner.invoke(
            pytest.test_run.main, [
                self.plugin
            ]
        )
        assert result.exit_code == 0
        assert 'Usage: main test-plugin' in result.output

    def test_delete_non_existing_pype(self):  # noqa: D102
        result = pytest.test_run.runner.invoke(
            pytest.test_run.main, [
                self.plugin, '--delete-pype', 'nan'
            ]
        )
        assert result.exit_code == 1
        assert 'No such pype' in result.output

    def test_create_and_delete_pype(self):  # noqa: D102
        result = pytest.test_run.runner.invoke(
            pytest.test_run.main, [
                self.plugin, '--create-pype', 'test'
            ]
        )
        assert result.exit_code == 0
        assert 'Created new pype' in result.output

        result = pytest.test_run.runner.invoke(
            pytest.test_run.main, [
                self.plugin, '--delete-pype', 'test'
            ]
        )
        assert result.exit_code == 0
        assert 'Deleted pype' in result.output
