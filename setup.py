#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Package installer script."""

from io import open
from os import environ, path

from setuptools import find_packages, setup

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'),
          encoding='utf-8') as f:
    long_description = f.read()

# Configure shell command
custom_shell_command = environ.get('PYPE_CUSTOM_SHELL_COMMAND', None)
shell_command = custom_shell_command if custom_shell_command else 'pype'
console_scripts = [f'{shell_command}=pype.__main__:main']

setup(
    # Basic project information
    name='pype-cli',
    version='0.5.4',
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
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
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
