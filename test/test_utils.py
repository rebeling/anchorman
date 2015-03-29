#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from anchorman.utils import sort_longest_match_first
from anchorman.utils import validate_input


def test_anchorman_utils_validate_input():

    args = ()
    success, values = validate_input(args)
    assert success == False
    assert values == "arguments text and links missing"

    args = ('wefe', 'wefwef')
    success, values = validate_input(args)
    assert success == False
    assert values == "links (second argument) should be list"

    args = (['wefe'], 'wefwef')
    success, values = validate_input(args)
    assert success == False
    assert values == "text (first argument) should be str/unicode"

    args = (['wefe'])
    success, values = validate_input(args)
    assert success == False
    assert values == "second argument is missing"

    args = ('wefe', [])
    success, values = validate_input(args)
    assert success == True
    assert values == args


def test_anchorman_utils_sort_longest_match_first():

    links = [{'boom': {}}, {'boombastic': {}}]
    sorted_links = sort_longest_match_first(links)
    assert sorted_links == [{'boombastic': {}}, {'boom': {}}]

