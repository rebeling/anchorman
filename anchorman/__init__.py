# -*- coding: utf-8 -*-
"""Provide first level access to the functions in main.
    >>> anchorman.annotate(...) instead of anchorman.main.annotate(...)

    I do not like the implicity, btu kenneth reitz does so in requests.
    And I love requests more than the implicity of this in here ;)
"""
from anchorman.main import annotate, clean
from anchorman.configuration import get_config
