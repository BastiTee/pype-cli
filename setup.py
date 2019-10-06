#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Package installer script."""

from io import open
from json import load
from os import environ, path

from setuptools import find_packages, setup

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'),
          encoding='utf-8') as f:
    long_description = f.read()

# Default console script
console_scripts = ['pype=pype.__main__:main']
# If present add custom shell command from configuration
try:
    config_json = load(open(environ.get('PYPE_CONFIGURATION_FILE'), 'r'))
    shell_command = config_json['core_config']['shell_command']
    console_scripts.append('{}=pype.__main__:main'.format(shell_command))
except Exception:
    pass  # Just continue regularily if nothing was found

setup(
    # Basic project information
    name='pype-cli',
    version='0.3.3-SNAPSHOT',
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
    entry_points={
        'console_scripts': console_scripts
    },
    # Licensing and copyright
    license='Apache 2.0'
)
