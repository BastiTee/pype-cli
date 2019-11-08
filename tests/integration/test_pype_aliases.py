# -*- coding: utf-8 -*-
"""$ pype --aliases."""

from tests import create_runner, create_test_env, invoke_runner, reload_config


class TestCLIPypeAliases:  # noqa: D101

    def test_no_aliases_present(self):  # noqa: D102
        test_run = invoke_runner('%MAIN%', '--aliases')
        assert test_run.result.exit_code == 0
        assert not test_run.result.output.strip()

    def test_unregister_non_existing_alias(self):  # noqa: D102
        test_run = invoke_runner(
            '%MAIN%',
            ['--unregister-alias', 'notpresent'])
        assert test_run.result.exit_code == 1
        assert 'No aliases registered' in test_run.result.output

    def test_registered_alias_found_in_config(self):  # noqa: D102
        with create_test_env() as test_env:
            test_run = create_runner(
                test_env,
                '%MAIN%',
                [
                    '--register-alias', 'myalias', 'pype.config',
                    'plugin-register'
                ])
            assert test_run.result.exit_code == 0
            assert 'Configured alias: myalias' in test_run.result.output
            result_configuration = reload_config(test_run)
            assert len(result_configuration['aliases']) == 1
            assert result_configuration['aliases'][0]['alias'] == 'myalias'
            result = test_run.runner.invoke(
                test_run.main,
                ['--unregister-alias', 'myalias'])
            assert result.exit_code == 0
            assert 'Unregistered alias: myalias' in result.output
            result_configuration = reload_config(test_run)
            assert len(result_configuration['aliases']) == 0
