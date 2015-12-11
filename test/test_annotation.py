# -*- coding: utf-8 -*-
from anchorman.main import annotate
from anchorman.configure import get_config
from data import *


def test_annotate_tag():
    """Test annotate tag with default config."""

    annotated = annotate(p_text, elements)

    expected_result = '<p class="first">The <a class="anchorman" href="/wiki/queick" style="color:blue;cursor:pointer;" type="term">qüick</a> brown <a class="anchorman" href="/wiki/fox" style="color:blue;cursor:pointer;" type="animal">fox</a> jumps</p> <p>over the <a class="anchorman" href="/wiki/lazy" style="color:blue;cursor:pointer;" type="term">lazy</a> <a class="anchorman" href="/wiki/dog" style="color:blue;cursor:pointer;" type="animal">dog</a> in <a class="anchorman" href="/wiki/los-angeles" style="color:blue;cursor:pointer;" type="city">Los Angeles</a>.</p>'
    assert annotated == expected_result


def test_annotate_highlight():
    """Test annotate with default config, but mode highlight."""

    cfg = get_config()
    cfg['setting']['mode'] = 'highlight'
    cfg['setting']['filter_by_value'] = {"score": 10.0}
    rpa = {'replaces_per_attribute': {'number_of_items': 1, 'attribute_key': 'type'}}
    cfg['setting'].update(rpa)

    annotated = annotate(p_text, elements, config=cfg)
    expected_result = '<p class="first">The qüick brown ${fox} jumps</p> <p>over the lazy dog in ${Los Angeles}.</p>'
    assert annotated == expected_result


def test_annotate_unknown():
    """Test annotate with default config, but mode hocuspocus."""

    cfg = get_config()
    cfg['setting']['mode'] = 'hocuspocus'

    try:
        annotated = annotate(p_text, elements, config=cfg)
    except Exception, e:
        assert type(e) == KeyError


def test_annotate_coreferencer():
    """Test annotate with default config, but mode coreferencer."""

    cfg = get_config()
    cfg['setting']['mode'] = 'coreferencer'

    try:
        annotated = annotate(p_text, elements, config=cfg)
    except Exception, e:
        assert type(e) == NotImplementedError

