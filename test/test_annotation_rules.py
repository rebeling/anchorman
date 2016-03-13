# -*- coding: utf-8 -*-
from anchorman import annotate, get_config
from anchorman.configuration import parse_yaml

DATA = parse_yaml('data.yaml', loaded_from=__file__)


def test_annotation_rules1():
    """Test annotate highlight with overwritten config."""

    cfg = get_config()

    overwrite = {
        'mode': 'highlight',
        'replaces_at_all': 3,
        'text_unit': {
            'number_of_items': 5,
            'key': 't',
            'name': 'text'}
    }
    cfg['setting'].update(overwrite)

    text = DATA['text'].encode('utf-8')
    highlight_elements = DATA['elements']
    annotated = annotate(text, highlight_elements, config=cfg)

    text_annotated = DATA['text_annotated_rule1'].encode('utf-8')
    assert annotated == text_annotated


def test_annotate_highlight_rules2():
    """Test annotate highlight with overwritten config."""

    cfg = get_config()

    overwrite = {
        'mode': 'highlight',
        'replaces_at_all': 2,
        'case_sensitive': False,
        'text_unit': {
            'key': 't',
            'name': 'text'}
    }
    cfg['setting'].update(overwrite)

    text2 = DATA['text2'].encode('utf-8')
    highlight_elements = DATA['elements']
    annotated = annotate(text2, highlight_elements, config=cfg)

    text_annotated = DATA['text_annotated_rule2'].encode('utf-8')
    assert annotated == text_annotated
