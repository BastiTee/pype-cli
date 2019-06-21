# -*- coding: utf-8 -*-
"""Print current pype version."""

import pkg_resources

from pype.core import get_pype_basepath

if __name__ == '__main__':
    base_path = get_pype_basepath()
    version = pkg_resources.get_distribution('pype-cli').version
    print('{} @ {}'.format(version, base_path))
