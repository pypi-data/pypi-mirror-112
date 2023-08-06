#!/usr/bin/env python3

import os
import sys
import glob

from pathlib import Path
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

readme = ''

entries = []
entries.append("vulseek = vulseek.cli.main:cli") #.format(cmd_file=cmd_file, cmd_name=cmd_name))

setup(
    name='vulseek',
    version='0.0.4',
    description='Vulseek Command Line Interface',
    long_description=readme,
    long_description_content_type='text/x-rst',
    author='Fabian Martinez Portantier',
    author_email='fportantier@securetia.com',
    url='https://gitlab.com/securetia/vulseek/cli',
    license='BSD 3-clause',
    install_requires=[
        'click',
        'requests',
    ],
    tests_require=[
        'pytest',
        'pytest-runner',
    ],
    entry_points={
        'console_scripts': entries,
    },
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.8",
    ],
    packages=['vulseek.cli'],
    include_package_data=True,
    keywords=['security'],
    zip_safe=False,
    test_suite='py.test',
)
