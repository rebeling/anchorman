#!/usr/bin/env python

from setuptools import setup

setup(
    name='tagger',
    version='1.0',
    description='Tag text in HTML documents',
    author='Retresco',
    packages=['tagger'],
    install_requires=["lxml"],
    tests_require=["pytest"]
)
