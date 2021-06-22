#!/usr/bin/env python

from __future__ import print_function
from setuptools import setup, find_packages
from glob import glob
import os
from sparrow.file_ops import yaml_load

pkgname = "sparrow-tool"
pkgdir = "sparrow"

version_config = yaml_load(os.path.join(pkgdir, "version-config.yaml"))
name, version = version_config['name'], version_config['version']

with open(glob('requirements.txt')[0], encoding='utf-8') as f:
    all_reqs = f.read().split('\n')
install_requires = [x.strip() for x in all_reqs]

with open("README.md", "r", encoding='utf-8') as fr:
    long_description = fr.read()

setup(name=name,
      version=version,
      package_data={
          pkgdir: [
              '*.yaml', '*.yml',
          ],
      },
      description="Python Common Function Tool Set.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="K.y",
      author_email="beidongjiedeguang@gmail.com",
      url="https://github.com/beidongjiedeguang/sparrow",
      license="MIT",
      install_requires=install_requires,
      classifiers=[
          'Operating System :: OS Independent',
          'Intended Audience :: Developers',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
      ],
      keywords=[
          'Tools', 'Mathematics', 'Machine Learning',
      ],
      packages=find_packages()
      )

