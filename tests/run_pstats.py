#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Format profiling output file.

https://docs.python.org/3.7/library/profile.html#instant-user-s-manual
"""

import pstats
from os import path
from pstats import SortKey

if __name__ == '__main__':
    src_file = path.join(
        path.dirname(path.abspath(__file__)), 'profile.obj')
    p = pstats.Stats(src_file)
    p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(25)
