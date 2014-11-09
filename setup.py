#!/usr/bin/env python

from setuptools import setup

setup(
    name='anchorman',
    version='0.0.1',
    description='link text in HTML documents',
    author='Tarn Barford',
    packages=['anchorman'],
    install_requires=['lxml'],
    tests_require=['pytest', 'pytest-cov']
)
