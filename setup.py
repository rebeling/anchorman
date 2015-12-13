# -*- coding: utf-8 -*-
from setuptools import setup
import yaml
import os
import sys

config = yaml.load(open('etc/conf.yaml', 'r').read())

cwd = os.getcwd()
project_root = os.path.dirname(cwd)
readme = open(project_root + '/anchorman/readme.rst', 'rt').read()
requirements = open(project_root + '/anchorman/requirements.txt', 'rt').read()


setup(
    name=config['name'],
    version=config['version'],
    author=config['author'],
    author_email=config.get('author_email'),
    url=config.get('url'),
    description=readme,
    packages=[config['name']],
    install_requires=[
        line.split('==')[0]
        for line in requirements.split('\n')
    ]
)
