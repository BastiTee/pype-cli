# -*- coding: utf-8 -*-
"""$ pype --aliases."""

from tests import create_runner, create_test_env, invoke_runner, reload_config


class TestCLIPypeAliases:  # noqa: D101

    def test_no_aliases_present(self) -> None:  # noqa: D102
        test_run = invoke_runner('%MAIN%', ['--aliases'])
        assert test_run.result.exit_code == 0
        assert not test_run.result.output.strip()

    def test_unregister_non_existing_alias(self) -> None:  # noqa: D102
        test_run = invoke_runner(
            '%MAIN%',
            ['--alias-unregister', 'notpresent'])
        assert test_run.result.exit_code == 2
        assert (
            'Error: Invalid value for \'--alias-unregister\''
            in test_run.result.output
        )

    def test_registered_alias_found_in_config(self) -> None:  # noqa: D102
        with create_test_env() as test_env:
            test_run = create_runner(
                test_env,
                '%MAIN%',
                [
                    '--alias-register', 'myalias', 'pype.config',
                    'plugin-register'
                ])
            assert test_run.result.exit_code == 0
            assert 'Configured alias: myalias' in test_run.result.output
            result_configuration = reload_config(test_run)
            assert len(result_configuration['aliases']) == 1
            assert result_configuration['aliases'][0]['alias'] == 'myalias'
            result = test_run.runner.invoke(
                test_run.reload_and_get_main,
                ['--alias-unregister', 'myalias'])
            assert result.exit_code == 0
            assert 'Unregistered alias: myalias' in result.output
            result_configuration = reload_config(test_run)
            assert len(result_configuration['aliases']) == 0
