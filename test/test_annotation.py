# -*- coding: utf-8 -*-
from anchorman.main import annotate
from anchorman.main import clean
from anchorman.configuration import get_config
from data import *


def test_schema_dot_org():
    """Test annotate tag with schema dot org specs config."""

    cfg = get_config()
    unit = {'key': 't', 'name': 'text'}
    cfg['setting']['text_unit'].update(unit)
    cfg['markup'] = {'tag': {'tag': 'div'}}

    annotated1 = annotate(s_text, s1_elements, config=cfg)
    expected_result1 = '<div itemscope itemtype="http://schema.org/Person">Angela Merkel, CDU, Bundeskanzlerin</div>'
    assert annotated1 == expected_result1

    annotated2 = annotate(annotated1, s11_elements, config=cfg)
    expected_result2 = '<div itemscope itemtype="http://schema.org/Person">Angela Merkel, <div itemscope itemtype="http://schema.org/Organization">CDU</div>, Bundeskanzlerin</div>'
    assert annotated2 == expected_result2

    cfg3 = cfg.copy()
    cfg3['markup'] = {'tag': {'tag': 'span'}}
    annotated3 = annotate(annotated2, s2_elements, config=cfg3)
    expected_result3 = '<div itemscope itemtype="http://schema.org/Person"><span itemprop="name">Angela Merkel</span>, <div itemscope itemtype="http://schema.org/Organization"><span itemprop="name">CDU</span></div>, <span itemprop="jobtitle">Bundeskanzlerin</span></div>'
    assert annotated3 == expected_result3

    success, cleared_text = clean(annotated3, config=cfg3)
    assert success
    assert expected_result2 == cleared_text

    success, cleared_text = clean(cleared_text, config=cfg)
    assert success
    assert s_text == cleared_text


def test_annotate_tag():
    """Test annotate tag with default config."""

    annotated = annotate(p_text, elements)

    expected_result = '<p class="first">The <a class="anchorman" href="/wiki/queick" style="color:blue;cursor:pointer;" type="term">qüick</a> brown <a class="anchorman" href="/wiki/fox" style="color:blue;cursor:pointer;" type="animal">fox</a> jumps</p> <p>over the <a class="anchorman" href="/wiki/lazy" style="color:blue;cursor:pointer;" type="term">lazy</a> <a class="anchorman" href="/wiki/dog" style="color:blue;cursor:pointer;" type="animal">dog</a> in <a class="anchorman" href="/wiki/los-angeles" style="color:blue;cursor:pointer;" type="city">Los Angeles</a>.</p>'
    assert annotated == expected_result

    success, cleared_text = clean(annotated)
    assert success
    assert p_text == cleared_text


def test_annotate_highlight():
    """Test annotate with default config, but mode highlight."""

    cfg = get_config()
    cfg['setting']['mode'] = 'highlight'
    cfg['setting']['filter_by_value'] = {"score": 10.0}
    rpa = {'replaces_per_attribute': {'number_of_items': 1, 'attribute_key': 'type'}}
    cfg['setting'].update(rpa)

    annotated = annotate(p_text, elements, config=cfg)
    expected_result = '<p class="first">The qüick brown ${{fox}} jumps</p> <p>over the lazy dog in ${{Los Angeles}}.</p>'

    assert annotated == expected_result

    success, cleared_text = clean(annotated, config=cfg)
    assert success
    assert p_text == cleared_text


def test_annotate_unknown():
    """Test annotate with default config, but mode hocuspocus."""

    cfg = get_config()
    cfg['setting']['mode'] = 'hocuspocus'

    try:
        _ = annotate(p_text, elements, config=cfg)
    except Exception, e:
        assert type(e) == KeyError


def test_annotate_coreferencer():
    """Test annotate with default config, but mode coreferencer."""

    cfg = get_config()
    cfg['setting']['mode'] = 'coreferencer'

    try:
        _ = annotate(p_text, elements, config=cfg)
    except Exception, e:
        assert type(e) == NotImplementedError
