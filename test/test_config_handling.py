# -*- coding: utf-8 -*-
import pytest
from yaml import YAMLError
from anchorman.configuration import parse_yaml


def test_parse_yaml():

    DATA = parse_yaml('../etc/config.yaml', loaded_from=__file__)
    assert isinstance(DATA, dict)


def test_yaml_io_error():

    with pytest.raises(IOError):
        _ = parse_yaml('nofilelikethis.yaml')


def test_yaml_parsing_error():

    with pytest.raises(YAMLError):
        _ = parse_yaml('test_config_handling.py', loaded_from=__file__)
