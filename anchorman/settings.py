# -*- coding: utf-8 -*-
import os
import yaml
from codecs import open
from anchorman.utils import log
import logging
import logging.config


def setup_logging(
        default_path='../config/logging.yml', default_level=logging.INFO,
        env_key='LOG_CFG'):
    """Setup logging configuration"""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def parse_yaml(filepath, loaded_from=__file__):
    """Get and parse yaml from absolute path."""
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
    """Load default configuration.

    :param include_project_config:
    """
    default = parse_yaml("../config/setup.yml")
    setup_logging()
    return default
