# -*- coding: utf-8 -*-
"""$ pype --aliases.

We need to delay the import of pype.__main__ until we set the environment
variables correctly. That is why tests.invoke_isolated_test gets called
with a string instead of a module.
"""


from tests import invoke_isolated_test, load_config_from_test


class TestCLIPypeAliases:  # noqa: D101

    def test_no_aliases_present(self):  # noqa: D102
        test_run = invoke_isolated_test('main', '--aliases')
        assert test_run.result.exit_code == 0
        print(test_run.result.output)
        assert not test_run.result.output.strip()

    def test_unregister_non_existing_alias(self):  # noqa: D102
        # We need to delay import of __main__.main to set environment first
        test_run = invoke_isolated_test(
            'main',
            ['--unregister-alias', 'notpresent'])
        assert test_run.result.exit_code == 1
        assert 'No aliases registered' in test_run.result.output

    def test_registered_alias_found_in_config(self):  # noqa: D102
        test_run = invoke_isolated_test(
            'main',
            ['--register-alias', 'myalias', 'pype.config', 'plugin-register'])
        assert test_run.result.exit_code == 0
        assert 'Configured alias: myalias' in test_run.result.output
        result_configuration = load_config_from_test(test_run)
        assert len(result_configuration['aliases']) == 1
        assert result_configuration['aliases'][0]['alias'] == 'myalias'
        test_run = invoke_isolated_test(
            'main',
            ['--unregister-alias', 'myalias'])
        assert test_run.result.exit_code == 0
        assert 'Unregistered alias: myalias' in test_run.result.output
        result_configuration = load_config_from_test(test_run)
        assert len(result_configuration['aliases']) == 0
