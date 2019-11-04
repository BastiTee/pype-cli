# -*- coding: utf-8 -*-
"""$ pype."""


from pype import __main__
from pype.config import __doc__ as config_doc

from tests import invoke_isolated_runner


class TestCLIPype:  # noqa: D101

    def test_no_pype_selected(self):  # noqa: D102
        result, _ = invoke_isolated_runner(__main__.main)
        assert result.exit_code == 0
        assert 'No pype selected.' in result.output

    def test_list_pypes(self):  # noqa: D102
        for opt in ['-l', '--list-pypes']:
            result, _ = invoke_isolated_runner(__main__.main, opt)
            assert result.exit_code == 0
            assert config_doc in result.output

    def test_help_page(self):  # noqa: D102
        for opt in ['-h', '--help']:
            result, _ = invoke_isolated_runner(__main__.main, opt)
            assert result.exit_code == 0
            assert __main__.__doc__ in result.output
