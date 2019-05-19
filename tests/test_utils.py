# -*- coding: utf-8 -*-

from pype.util.misc import (get_from_json_or_default)


class TestUtils:

    def test_get_from_json_or_default__noneInput(self):
        value = get_from_json_or_default(None, None, None)
        assert not value

    def test_get_from_json_or_default__noneInputWithEmptyBreadcrumb(self):
        value = get_from_json_or_default(None, '', None)
        assert not value

    def test_get_from_json_or_default__noneInputWithBreadcrumb(self):
        value = get_from_json_or_default(None, 'test', None)
        assert not value

    def test_get_from_json_or_default__noneInputWithBreadcrumbCustom(self):
        value = get_from_json_or_default(None, 'test', 'custom')
        assert value == 'custom'

    def test_get_from_json_or_default__firstLevelBreadcrumb(self):
        value = get_from_json_or_default({
            'test': 'response'
        }, 'test', 'custom')
        assert value == 'response'

    def test_get_from_json_or_default__secondLevelBreadcrumb(self):
        value = get_from_json_or_default({
            'test': {
                'subtest': 'response'
            }
        }, 'test.subtest', 'default'
        )
        assert value == 'response'

    def test_get_from_json_or_default__secondLevelBreadcrumbMiss(self):
        value = get_from_json_or_default({
            'test': {
                'subtest': 'response'
            }
        }, 'test.subtestmiss', 'default'
        )
        assert value == 'default'
