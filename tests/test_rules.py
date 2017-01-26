# -*- coding: utf-8 -*-
from anchorman import annotate, clean, get_config
from utils import fix_bs4_parsing_spaces
from tests.data.dummy import LINKS


def test_annotation_rules():
    """Test annotate elements with default and manipulated config."""

    RLINKS = [
        {"A":   {"type": "letterA", "score": 42}},
        {"AA":  {"type": "letterA", "score": 42}},
        {"AAA": {"type": "letterA", "score": 42}},
        {"B":   {"type": "letterB", "score": 42}},
        {"BB":  {"type": "letterB", "score": 42}},
        {"BBB": {"type": "letterB", "score": 42}},
        {"C":   {"type": "letterC", "score": 42}},
        {"CC":  {"type": "letterC", "score": 42}},
        {"CCC": {"type": "letterC", "score": 42}},
        {"D":   {"type": "letterD", "score": 42}},
        {"DD":  {"type": "letterD", "score": 42}},
        {"DDD": {"type": "letterD", "score": 42}},
        {"E":   {"type": "letterE", "score": 42}},
        {"EE":  {"type": "letterE", "score": 42}},
        {"EEE": {"type": "letterE", "score": 42}}]

    RTEXT = """<div>
    <p id="1">lala A la lala AA BB B la C lalala DDD D E</p>
    <p id="2">la E EE AA lal CC C la la BB la DD D lala EE la</p>
    <p id="3">B la BB EEE A la CCC B la DDD C lala AAA D la BBB E</p>
    </div>
    """

    cfg = get_config()    
    cfg['settings']['return_applied_links'] = True

    cfg['markup'] = {
        'anchor_pattern': '<a class="anchorman" type="{type}">{token}</a>',
        'decorate_anchor_key': 'the_anchor',
    }

    number_of_links_to_apply = 5
    cfg['rules']['replaces_at_all'] = number_of_links_to_apply
    annotated, applied, rest = annotate(RTEXT, RLINKS, config=cfg)
    assert len(applied) == number_of_links_to_apply

    cfg['rules']['replaces_at_all'] = number_of_links_to_apply
    cfg['rules']['items_per_unit'] = 1
    annotated, applied, rest = annotate(RTEXT, RLINKS, config=cfg)
    assert len(applied) == 3

    cfg['rules']['items_per_unit'] = 2
    cfg['rules']['replaces_at_all'] = None
    cfg['rules']['replaces_by_attribute'] = {
        'key': 'type', 'value_per_unit': 1}
    annotated, applied, rest = annotate(RTEXT, RLINKS, config=cfg)
    assert len(applied) == 6

    cfg['rules']['items_per_unit'] = 2
    cfg['rules']['replaces_at_all'] = None
    cfg['rules']['n_times_key_value'] = {
        'key': 'type',
        'value_overall': 1
    }
    del cfg['rules']['replaces_by_attribute']
    annotated, applied, rest = annotate(RTEXT, RLINKS, config=cfg)
    assert len(applied) == 5

    # filter_by_attribute:

    #     # strict: false   # check only one, true only valid if all match
    #     attributes:
    #         - key: type
    #           value: animal
    #         - key: score
    #           value: 10

    cfg = get_config()
    cfg['settings']['return_applied_links'] = True
    cfg['rules']['filter_by_attribute'] = {
        'attributes': [
            {'type': 'letterA'},
            {'score': 42}
        ]
    }
    annotated, applied, rest = annotate(RTEXT, RLINKS, config=cfg)
    assert len(applied) == 0

    # # number_of_links_to_apply = 5
    # # cfg['settings']['return_applied_links'] = True
    # # cfg['rules']['replaces_at_all'] = number_of_links_to_apply
    # # annotated, applied, rest = annotate(text, LINKS, config=cfg)
    # # assert len(applied) == number_of_links_to_apply


    # # annotated, applied, rest = annotate(text, LINKS, config=cfg)
    # # assert len(applied) == number_of_links_to_apply
