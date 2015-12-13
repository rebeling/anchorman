# -*- coding: utf-8 -*-
from setuptools import setup
import yaml
import os
import sys

# wat?
config = yaml.load(open('etc/conf.yaml', 'r').read())

try:
    dir_here = os.path.dirname(os.path.abspath(__file__))
    print dir_here
    readme = open(dir_here + '/readme.rst', 'rt').read()
    requirements = open(dir_here + '/requirements.txt', 'rt').read()
except:
    readme = ""
    requirements = ""


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
