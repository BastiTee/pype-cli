# -*- coding: utf-8 -*-
"""$ pype pype-config plugin-register/plugin-unregister."""

from pype.config import plugin_register, plugin_unregister

from tests import invoke_isolated_runner


class TestCLIPypePluginRegister:  # noqa: D101

    def test_register_without_name(self):  # noqa: D102
        result, _ = invoke_isolated_runner(plugin_register.main)
        assert result.exit_code == 2
        assert 'Missing option "--name"' in result.output

    def test_register_without_path(self):  # noqa: D102
        result, _ = invoke_isolated_runner(
            plugin_register.main, ['--name', 'test'])
        assert result.exit_code == 2
        assert 'Missing option "--path"' in result.output

    def test_register_without_create(self):  # noqa: D102
        result, _ = invoke_isolated_runner(
            plugin_register.main,
            ['--name', 'a_random_plugin', '--path', '.'])
        assert result.exit_code == 1
        assert 'Could not find a python module' in result.output

    def test_register_with_create(self):  # noqa: D102
        result, _ = invoke_isolated_runner(
            plugin_register.main,
            ['--name', 'a_random_plugin', '--path', '.', '--create'])
        assert result.exit_code == 0
        assert 'successfully created' in result.output

    def test_register_unregister_and_reregister(self):  # noqa: D102
        result, runner = invoke_isolated_runner(
            plugin_register.main,
            ['--name', 'a_random_plugin', '--path', '.', '--create'])
        assert result.exit_code == 0
        assert 'successfully created' in result.output
        result = runner.invoke(
            plugin_unregister.main,
            ['--name', 'a_random_plugin'])
        assert result.exit_code == 0
        assert 'successfully unregistered' in result.output
        result = runner.invoke(
            plugin_register.main,
            ['--name', 'a_random_plugin', '--path', '.'])
        assert result.exit_code == 0
        assert 'successfully registered' in result.output
