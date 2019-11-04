# -*- coding: utf-8 -*-
"""$ pype pype-config plugin-register/plugin-unregister."""

from pype.config import plugin_register, plugin_unregister

from tests import invoke_isolated_test


class TestCLIPypePluginRegister:  # noqa: D101

    def test_register_without_name(self):  # noqa: D102
        test_run = invoke_isolated_test(plugin_register.main)
        assert test_run.result.exit_code == 2
        assert 'Missing option "--name"' in test_run.result.output

    def test_register_without_path(self):  # noqa: D102
        test_run = invoke_isolated_test(
            plugin_register.main, ['--name', 'test'])
        assert test_run.result.exit_code == 2
        assert 'Missing option "--path"' in test_run.result.output

    def test_register_without_create(self):  # noqa: D102
        test_run = invoke_isolated_test(
            plugin_register.main,
            ['--name', 'a_random_plugin', '--path', '.'])
        assert test_run.result.exit_code == 1
        assert 'Could not find a python module' in test_run.result.output

    def test_register_with_create(self):  # noqa: D102
        test_run = invoke_isolated_test(
            plugin_register.main,
            ['--name', 'a_random_plugin', '--path', '.', '--create'])
        assert test_run.result.exit_code == 0
        assert 'successfully created' in test_run.result.output

    def test_register_unregister_and_reregister(self):  # noqa: D102
        test_run = invoke_isolated_test(
            plugin_register.main,
            ['--name', 'a_random_plugin', '--path', '.', '--create'])
        assert test_run.result.exit_code == 0
        assert 'successfully created' in test_run.result.output
        result = test_run.runner.invoke(
            plugin_unregister.main,
            ['--name', 'a_random_plugin'])
        assert result.exit_code == 0
        assert 'successfully unregistered' in result.output
        result = test_run.runner.invoke(
            plugin_register.main,
            ['--name', 'a_random_plugin', '--path', '.'])
        assert result.exit_code == 0
        assert 'successfully registered' in result.output
