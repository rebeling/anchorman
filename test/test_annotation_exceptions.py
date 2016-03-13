# -*- coding: utf-8 -*-
from anchorman import annotate, clean, get_config
from anchorman.configuration import parse_yaml
import pytest

DATA = parse_yaml('data.yaml', loaded_from=__file__)


def test_markup_unknown():
    """Test annotate with key in settings but not in markup."""

    cfg = get_config()
    cfg['setting'].update({'mode': 'hocuspocus'})
    two_paragraphs = DATA['two_paragraphs'].encode('utf-8')
    link_elements = DATA['elements']

    try:
        _ = annotate(two_paragraphs, link_elements, config=cfg)
    except Exception, e:
        assert type(e) == KeyError


def test_clean_annotatation():
    """Test removal by specific mode of annotation."""

    cfg = get_config()
    cfg['setting'].update({'mode': 'highlight'})
    two_paragraphs = DATA['two_paragraphs'].encode('utf-8')
    highlight_elements = DATA['elements']
    annotated = annotate(two_paragraphs, highlight_elements, config=cfg)

    # change config
    cfg['setting'].update({'mode': 'unknown'})

    with pytest.raises(NotImplementedError):
        success, cleared_text = clean(annotated, config=cfg)
