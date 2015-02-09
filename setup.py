#!/usr/bin/env python

import anchorman

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from codecs import open

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()


setup(
    name=anchorman.__title__,
    version=anchorman.__version__,
    description='link text in HTML documents',
    long_description=readme,
    author=anchorman.__author__,
    author_emai=anchorman.__author_email__,
    url=anchorman.__url__,
    license=anchorman.__license__,
    packages=['anchorman'],
    package_data={'': ['LICENSE', 'NOTICE']},
    package_dir={'anchorman': 'anchorman'},
    include_package_data=True,
    install_requires=['lxml'],
    tests_require=['pytest', 'pytest-cov']
)
