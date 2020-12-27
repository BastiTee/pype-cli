# -*- coding: utf-8 -*-
"""$ pype."""

from pype.config import __doc__ as config_doc
from tests import invoke_runner


class TestCLIPype:  # noqa: D101

    def test_no_pype_selected(self) -> None:  # noqa: D102
        test_run = invoke_runner('%MAIN%')
        assert test_run.result.exit_code == 0
        assert 'No pype selected.' in test_run.result.output

    def test_list_pypes(self) -> None:  # noqa: D102
        for opt in ['-l', '--list-pypes']:
            test_run = invoke_runner('%MAIN%', [opt])
            assert test_run.result.exit_code == 0
            assert config_doc in test_run.result.output

    def test_help_page(self) -> None:  # noqa: D102
        for opt in ['-h', '--help']:
            test_run = invoke_runner('%MAIN%', [opt])
            assert test_run.result.exit_code == 0
            assert ('PYPE - A command-line tool for command-line tools.'
                    in test_run.result.output)
