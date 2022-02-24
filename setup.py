#!/usr/bin/env python

from __future__ import print_function
from setuptools import setup

pkgname = "sparrow-tool"
pkgdir = "sparrow"

setup(
    setup_requires=['pbr>=1.9', 'setuptools>=50.3.2', 'setuptools-declarative-requirements'],
    pbr=True,
    package_data={
        pkgdir: [
            '*.yaml', '*.yml',
        ],
    },
)
