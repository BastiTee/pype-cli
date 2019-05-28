# -*- coding: utf-8 -*-
"""Pype miscellaneous utils tests."""

from pype.util.misc import get_from_json_or_default


class TestUtils():
    """Pype miscellaneous utils tests."""

    def test_get_from_json_or_default__noneInput(self):
        """get_from_json_or_default called with none-inputs."""
        value = get_from_json_or_default(None, None, None)
        assert not value

    def test_get_from_json_or_default__noneInputWithEmptyBreadcrumb(self):
        """get_from_json_or_default called with empty breadcrumb."""
        value = get_from_json_or_default(None, '', None)
        assert not value

    def test_get_from_json_or_default__noneInputWithBreadcrumb(self):
        """get_from_json_or_default called with breadcrumb but empty JSON."""
        value = get_from_json_or_default(None, 'test', None)
        assert not value

    def test_get_from_json_or_default__noneInputWithBreadcrumbCustom(self):
        """get_from_json_or_default called w/ crumb, empy JSON and default."""
        value = get_from_json_or_default(None, 'test', 'custom')
        assert value == 'custom'

    def test_get_from_json_or_default__firstLevelBreadcrumb(self):
        """get_from_json_or_default to resolve a first level entry."""
        value = get_from_json_or_default({
            'test': 'response'
        }, 'test', 'custom')
        assert value == 'response'

    def test_get_from_json_or_default__secondLevelBreadcrumb(self):
        """get_from_json_or_default to resolve a second level entry."""
        value = get_from_json_or_default({
            'test': {
                'subtest': 'response'
            }
        }, 'test.subtest', 'default'
        )
        assert value == 'response'

    def test_get_from_json_or_default__secondLevelBreadcrumbMiss(self):
        """get_from_json_or_default to miss a second level entry."""
        value = get_from_json_or_default({
            'test': {
                'subtest': 'response'
            }
        }, 'test.subtestmiss', 'default'
        )
        assert value == 'default'
