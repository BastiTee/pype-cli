# -*- coding: utf-8 -*-
"""$ pype."""


from pype import __main__
from pype.config import __doc__ as config_doc

from tests import invoke_isolated_test


class TestCLIPype:  # noqa: D101

    def test_no_pype_selected(self):  # noqa: D102
        test_run = invoke_isolated_test(__main__.main)
        assert test_run.result.exit_code == 0
        assert 'No pype selected.' in test_run.result.output

    def test_list_pypes(self):  # noqa: D102
        for opt in ['-l', '--list-pypes']:
            test_run = invoke_isolated_test(__main__.main, opt)
            assert test_run.result.exit_code == 0
            assert config_doc in test_run.result.output

    def test_help_page(self):  # noqa: D102
        for opt in ['-h', '--help']:
            test_run = invoke_isolated_test(__main__.main, opt)
            assert test_run.result.exit_code == 0
            assert __main__.__doc__ in test_run.result.output
