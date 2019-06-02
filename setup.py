#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Package installer script."""

from io import open
from os import environ, path

from pype.pype_constants import ENV_SHELL_COMMAND

from setuptools import find_packages, setup

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'),
          encoding='utf-8') as f:
    long_description = f.read()

shell_command = environ.get(ENV_SHELL_COMMAND, 'pype')

setup(
    # Basic project information
    name='pype-cli',
    version='0.1.3-SNAPSHOT',
    # Authorship and online reference
    author='Basti Tee',
    author_email='basti.tee@posteo.de',
    url='https://github.com/BastiTee/pype',
    # Detailed description
    description='A command-line tool for command-line tools',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='development',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    # Package configuration
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    python_requires='>=3.5',
    install_requires=[
        'click',
        'tabulate',
        'colorama',
        'pygments',
        'requests',
        'jsonschema',
        'progress'
    ],
    entry_points="""
        [console_scripts]
        """ + shell_command + """=pype.__main__:main
    """,
    # Licensing and copyright
    license='Apache 2.0'
)
