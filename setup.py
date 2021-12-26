#!/usr/bin/env python

from __future__ import print_function
from setuptools import setup, find_packages
import os


def yaml_load(filepath):
    from yaml import load
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader
    with open(filepath, 'r', encoding="utf-8") as stream:
        #     stream = stream.read()
        content = load(stream, Loader=Loader)
    return content


pkgname = "sparrow-tool"
pkgdir = "sparrow"

version_config = yaml_load(os.path.join(pkgdir, "version-config.yaml"))
name, version = version_config['name'], version_config['version']
setup(
    setup_requires=['pbr>=1.9', 'setuptools>=17.1'],
    pbr=True,
    package_data={
        pkgdir: [
            '*.yaml', '*.yml',
        ],
    },
)
