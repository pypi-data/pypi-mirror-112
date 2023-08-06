# -*- coding: utf-8 -*-

import os
import sys
from setuptools import find_packages
from setuptools import setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from seravo import __version__  # noqa: E402


def read_requirements(filename):
    with open(filename, 'r', encoding='utf-8') as reqfile:
        return [x for x in reqfile.readlines() if not x.startswith('#')]


setup(name='seravo',
      version=__version__,
      description='Shared libraries for Seravo',
      author='Seravo Oy',
      author_email='help@seravo.com',
      url='https://github.com/seravo/python-seravo/',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires=read_requirements('requirements.txt'))
