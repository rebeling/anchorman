#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from codecs import open

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='anchorman',
    version='0.0.2',
    description='Markup terms in text',
    long_description=readme,
    author='Tarn Barford',
    author_email='tarn@tarnbarford.net',
    url='https://github.com/tarnacious/anchorman',
    license='Apache 2.0',
    packages=['anchorman'],
    package_data={'': ['LICENSE', 'NOTICE']},
    package_dir={'anchorman': 'anchorman'},
    include_package_data=True,
    install_requires=['lxml'],
    tests_require=['pytest', 'pytest-cov']
)
