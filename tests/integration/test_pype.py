# -*- coding: utf-8 -*-
"""$ pype.

We need to delay the import of pype.__main__ until we set the environment
variables correctly. That is why tests.invoke_isolated_test gets called
with a string instead of a module.
"""


from pype.config import __doc__ as config_doc

from tests import invoke_isolated_test


class TestCLIPype:  # noqa: D101

    def test_no_pype_selected(self):  # noqa: D102
        test_run = invoke_isolated_test('main')
        assert test_run.result.exit_code == 0
        assert 'No pype selected.' in test_run.result.output

    def test_list_pypes(self):  # noqa: D102
        for opt in ['-l', '--list-pypes']:
            test_run = invoke_isolated_test('main', opt)
            assert test_run.result.exit_code == 0
            assert config_doc in test_run.result.output

    def test_help_page(self):  # noqa: D102
        for opt in ['-h', '--help']:
            test_run = invoke_isolated_test('main', opt)
            assert test_run.result.exit_code == 0
            assert ('PYPE - A command-line tool for command-line tools.'
                    in test_run.result.output)
