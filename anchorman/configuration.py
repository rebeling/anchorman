# -*- coding: utf-8 -*-
import os
import yaml
from codecs import open
from anchorman.logger import log


def parse_yaml(filepath, loaded_from=__file__):

    abspath = os.path.abspath(os.path.dirname(loaded_from))
    path = "/".join([abspath, filepath])
    try:
        yaml_data = yaml.load(open(path, 'r', 'utf-8'))
    except IOError, e:
        log("No yaml file found: %s" % e)
        raise IOError
    except yaml.YAMLError, e:
        log("Error in configuration file: %s" % e)
        raise yaml.YAMLError
    return yaml_data


def get_config(include_project_config=True):
    """Load default configuration."""

    default = parse_yaml("../etc/link.yaml")

    if include_project_config:
        conf = parse_yaml("../etc/config.yaml")
        default.update(conf)

    return default
