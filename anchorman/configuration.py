# -*- coding: utf-8 -*-
import os
import sys
import yaml
from codecs import open


def parse_yaml(filepath, loaded_from=__file__):
    abspath = os.path.abspath(os.path.dirname(loaded_from))
    path = "/".join([abspath, filepath])
    try:
        yaml_data = yaml.load(open(path, 'r', 'utf-8'))
        return yaml_data
    except IOError, e:
        sys.stdout.write("No yaml file found: %s" % e)
        raise IOError
    except yaml.YAMLError, e:
        sys.stdout.write("Error in configuration file: %s" % e)
        raise yaml.YAMLError


def get_config(project_conf=True):
    """Load default configuration."""

    default = parse_yaml("../etc/link.yaml")

    if project_conf:
        conf = parse_yaml("../etc/conf.yaml")
        default.update(conf)

    return default
