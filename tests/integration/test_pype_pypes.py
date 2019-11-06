# -*- coding: utf-8 -*-
"""$ pype <plugin> --create-pype/--delete-pype."""

from pype.config import plugin_register, plugin_unregister

import pytest

from tests import create_runner, create_test_env


class TestCLIPypePypes:  # noqa: D101

    @pytest.fixture(autouse=True, scope='module')
    def _run_around_tests(self):
        with create_test_env() as test_env:
            # Before all
            pytest.test_run = create_runner(
                test_env,
                plugin_register.main,
                ['--name', 'test_plugin', '--path', '.', '--create'])
            assert pytest.test_run.result.exit_code == 0
            assert 'successfully created' in pytest.test_run.result.output

            # Run test
            yield

            # After all
            result = pytest.test_run.runner.invoke(
                plugin_unregister.main,
                ['--name', 'test_plugin'])
            assert result.exit_code == 0
            assert 'successfully unregistered' in result.output

    def test_registered_plugin_found(self):  # noqa: D102
        result = pytest.test_run.runner.invoke(
            pytest.test_run.main
        )
        assert result.exit_code == 0
