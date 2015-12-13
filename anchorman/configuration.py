# -*- coding: utf-8 -*-
import os
import yaml


def get_config(project_conf=True):
    """Load default configuration."""

    path = os.path.abspath(os.path.dirname(__file__))
    default = yaml.load(open("{0}/{1}".format(path, '../etc/link.yaml'), 'r').read())

    if project_conf:
        conf = yaml.load(open("{0}/{1}".format(path, '../etc/conf.yaml'), 'r').read())
        default.update(conf)

    return default
