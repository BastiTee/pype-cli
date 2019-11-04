# -*- coding: utf-8 -*-
"""$ pype."""


from click.testing import CliRunner

from pype import __main__
from pype.config import __doc__ as config_doc

from tests import set_temporary_config_file


class TestCLIPype:
    """CLI pype tests."""

    def test_no_pype_selected(self):  # noqa: D102
        runner = CliRunner()
        set_temporary_config_file()
        with runner.isolated_filesystem():
            result = runner.invoke(__main__.main)
            assert result.exit_code == 0
            assert 'No pype selected.' in result.output

    def test_list_pypes(self):  # noqa: D102
        runner = CliRunner()
        set_temporary_config_file()
        with runner.isolated_filesystem():
            for opt in ['-l', '--list-pypes']:
                result = runner.invoke(__main__.main, opt)
                assert result.exit_code == 0
                assert config_doc in result.output

    def test_help_page(self):  # noqa: D102
        set_temporary_config_file()
        runner = CliRunner()
        with runner.isolated_filesystem():
            for opt in ['-h', '--help']:
                result = runner.invoke(__main__.main, opt)
                assert result.exit_code == 0
                assert __main__.__doc__ in result.output
