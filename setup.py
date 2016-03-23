# -*- coding: utf-8 -*-
from setuptools import setup
import yaml
import os

path = os.path.dirname(os.path.abspath(__file__))
config = yaml.load(file(path + '/etc/config.yaml', 'r'))


setup(
    name=config['name'],
    version=config['version'],
    author=config['author'],
    author_email=config.get('author_email'),
    url=config.get('url'),
    description=config.get('description'),
    keywords=config.get('keywords'),
    license=config.get('license'),
    packages=[config['name']],
    install_requires=[
        line.split('==')[0]
        for line in open('requirements.txt', 'rt').read().split('\n')
    ]
)
