# -*- coding: utf-8 -*-
from anchorman.main import annotate
from anchorman.configuration import get_config
from data import *


def test_annotate_highlight_settings():
    """Test annotate highlight with overwritten config."""

    cfg = get_config()
    cfg['setting']['mode'] = 'highlight'
    cfg['setting']['replaces_at_all'] = 3
    unit = {'number_of_items': 5, 'key': 't', 'name': 'text'}
    cfg['setting']['text_unit'].update(unit)

    annotated = annotate(t_text, elements, config=cfg)
    expected_result = 'The ${qüick} brown ${fox} jumps over the ${lazy} dog in Los Angeles.'
    assert annotated == expected_result


def test_annotate_highlight_settings_1():
    """Test annotate highlight with overwritten config."""

    cfg = get_config()
    cfg['setting']['mode'] = 'highlight'
    cfg['setting']['replaces_at_all'] = 2
    unit = {'number_of_items': 0, 'key': 't', 'name': 'text'}
    cfg['setting']['text_unit'].update(unit)

    annotated = annotate(t_text, elements, config=cfg)
    expected_result = 'The qüick brown fox jumps over the lazy dog in Los Angeles.'
    assert annotated == expected_result


def test_annotate_highlight_settings_2():
    """Test annotate highlight with overwritten config."""

    cfg = get_config()
    cfg['setting']['mode'] = 'highlight'
    unit = {'number_of_items': 1, 'key': 't', 'name': 'text'}
    cfg['setting']['text_unit'].update(unit)

    annotated = annotate(t_text, elements, config=cfg)
    expected_result = 'The ${qüick} brown fox jumps over the lazy dog in Los Angeles.'
    assert annotated == expected_result


def test_annotate_highlight_settings_raise_notimplementederror():
    """Test annotate highlight with overwritten config."""

    cfg = get_config()
    cfg['setting']['mode'] = 'highlight'
    unit = {'number_of_items': 1, 'key': 's', 'name': 'sentence'}
    cfg['setting']['text_unit'].update(unit)

    try:
        annotated = annotate(t_text, elements, config=cfg)
    except Exception, e:
        assert type(e) == NotImplementedError
