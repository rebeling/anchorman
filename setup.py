#!/usr/bin/env python
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from codecs import open
with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

version = ''
with open('anchorman/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='anchorman',
    version=version,
    description='Markup terms in text',
    long_description=readme,
    author='Tarn Barford, Matthias Rebel',
    author_email='matthias.rebel@gmail.com',
    url='https://github.com/rebeling/anchorman.git',
    license='Apache 2.0',
    packages=['anchorman'],
    package_data={'': ['LICENSE', 'NOTICE']},
    package_dir={'anchorman': 'anchorman'},
    include_package_data=True,
    install_requires=['lxml', 'regex'],
    tests_require=['pytest', 'pytest-cov']
)
