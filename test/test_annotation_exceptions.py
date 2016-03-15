# -*- coding: utf-8 -*-
from anchorman import annotate, clean, get_config
from anchorman.configuration import parse_yaml
import pytest

DATA = parse_yaml('data.yaml', loaded_from=__file__)


def test_markup_unknown():
    """Test annotate with key in settings but not in markup."""

    cfg = get_config()
    cfg['settings'].update({'mode': 'hocuspocus'})

    with pytest.raises(KeyError):
        _ = annotate('', DATA['elements'], config=cfg)


def test_clean_annotatation():
    """Test removal by specific mode of annotation."""

    cfg = get_config()
    cfg['settings'].update({'mode': 'highlight'})
    two_paragraphs = DATA['test_paragraphs']['content'].encode('utf-8')
    highlight_elements = DATA['elements']
    annotated = annotate(two_paragraphs, highlight_elements, config=cfg)

    # change config
    cfg['settings'].update({'mode': 'unknown'})

    with pytest.raises(NotImplementedError):
        success, cleared_text = clean(annotated, config=cfg)
