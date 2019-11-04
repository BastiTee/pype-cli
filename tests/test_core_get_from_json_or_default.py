# -*- coding: utf-8 -*-
"""pype.core.get_from_json_or_default."""

from pype.core import get_from_json_or_default


class TestCoreGetFromJsonOrDefault:
    """pype.core.get_from_json_or_default."""

    def test_noneinput(self):  # noqa: D102
        value = get_from_json_or_default(None, None, None)
        assert not value

    def test_noneinputwithemptybreadcrumb(self):  # noqa: D102
        value = get_from_json_or_default(None, '', None)
        assert not value

    def test_noneinputwithbreadcrumb(self):  # noqa: D102
        value = get_from_json_or_default(None, 'test', None)
        assert not value

    def test_noneinputwithbreadcrumbcustom(self):  # noqa: D102
        value = get_from_json_or_default(None, 'test', 'custom')
        assert value == 'custom'

    def test_firstlevelbreadcrumb(self):  # noqa: D102
        value = get_from_json_or_default({
            'test': 'response'
        }, 'test', 'custom')
        assert value == 'response'

    def test_secondlevelbreadcrumb(self):  # noqa: D102
        value = get_from_json_or_default({
            'test': {
                'subtest': 'response'
            }
        }, 'test.subtest', 'default'
        )
        assert value == 'response'

    def test_secondlevelbreadcrumbmiss(self):  # noqa: D102
        value = get_from_json_or_default({
            'test': {
                'subtest': 'response'
            }
        }, 'test.subtestmiss', 'default'
        )
        assert value == 'default'
