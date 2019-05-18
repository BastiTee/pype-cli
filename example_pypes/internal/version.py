#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Print current pype version."""

import subprocess
from pype.pype_core import get_pype_basepath

subprocess.run("""\
cd """ + get_pype_basepath() + """ && git rev-parse --verify --short HEAD
""", shell=True)
