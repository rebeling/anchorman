# -*- coding: utf-8 -*-
from setuptools import setup
import yaml

config = yaml.load(file('etc/conf.yaml', 'r'))


setup(
    name=config['name'],
    version=config['version'],
    author=config['author'],
    author_email=config.get('author_email'),
    url=config.get('url'),
    description='',
    license=config.get('license'),
    packages=[config['name']],
    install_requires=[
        line.split('==')[0]
        for line in open('requirements.txt', 'rt').read().split('\n')
    ]
)
