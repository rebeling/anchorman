# -*- coding: utf-8 -*-
from anchorman import annotate, clean, get_config
from anchorman.configuration import parse_yaml
import pytest

DATA = parse_yaml('data.yaml', loaded_from=__file__)


def test_annotate_tag():
    """Test annotate elements with default config.

    Take two paragraphs and create the default a tag for every item
    of elements.
    """

    two_paragraphs = DATA['test_paragraphs']['content'].encode('utf-8')
    link_elements = DATA['elements']
    annotated = annotate(two_paragraphs, link_elements)
    all_annotated = DATA['test_paragraphs']['results']['all_annotated'].encode('utf-8')
    assert annotated == all_annotated

    success, cleared_text = clean(annotated)
    assert success
    assert two_paragraphs == cleared_text


def test_annotate_highlight():
    """Test annotate with manipulated config and with mode highlight.

    Take two paragraphs and create a highlighted item for one item
    per paragraph of elements.
    """

    cfg = get_config()
    highlight = {
        'mode': 'highlight',
        'filter_by_value': {"score": 10.0},
        'replaces_per_attribute': {
            'number_of_items': 1,
            'attribute_key': 'type'}
    }
    cfg['settings'].update(highlight)
    two_paragraphs = DATA['test_paragraphs']['content'].encode('utf-8')
    highlight_elements = DATA['elements']
    annotated = annotate(two_paragraphs, highlight_elements, config=cfg)

    tpopa = DATA['test_paragraphs']['results']['one_per_paragrah_annotated'].encode('utf-8')
    assert annotated == tpopa

    success, cleared_text = clean(annotated, config=cfg)
    assert success
    assert two_paragraphs == cleared_text
