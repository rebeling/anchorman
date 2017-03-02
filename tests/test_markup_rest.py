# -*- coding: utf-8 -*-
from anchorman import annotate, clean, get_config
from tests.utils import fix_bs4_parsing_spaces
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
    </div>"""

    cfg = get_config()
    cfg['settings']['return_applied_links'] = True

    number_of_links_to_apply = 5
    cfg['rules']['replaces_at_all'] = number_of_links_to_apply

    cfg['markup'] = {
        'anchor_pattern': '<a class="anchorman">{token}</a>',
        'decorate_anchor_key': 'the_anchor',
        'decorate': {
            'decorate_pattern': '<span type="{type}">{the_anchor}</span>',
            'decorate_anchor_key': 'the_anchor'
        }
    }

    annotated, applied, rest = annotate(RTEXT, RLINKS, config=cfg)
    assert len(applied) == number_of_links_to_apply

    expected = """<div> <p id="1">lala <span type="letterA"><a class="anchorman">A</a></span> la lala <span type="letterA"><a class="anchorman">AA</a></span> <span type="letterB"><a class="anchorman">BB</a></span> <span type="letterB"><a class="anchorman">B</a></span> la <span type="letterC"><a class="anchorman">C</a></span> lalala <span type="letterD">DDD</span> <span type="letterD">D</span> <span type="letterE">E</span></p> <p id="2">la <span type="letterE">E</span> <span type="letterE">EE</span> <span type="letterA">AA</span> lal <span type="letterC">CC</span> <span type="letterC">C</span> la la <span type="letterB">BB</span> la <span type="letterD">DD</span> <span type="letterD">D</span> lala <span type="letterE">EE</span> la</p> <p id="3"><span type="letterB">B</span> la <span type="letterB">BB</span> <span type="letterE">EEE</span> <span type="letterA">A</span> la <span type="letterC">CCC</span> <span type="letterB">B</span> la <span type="letterD">DDD</span> <span type="letterC">C</span> lala <span type="letterA">AAA</span> <span type="letterD">D</span> la <span type="letterB">BBB</span> <span type="letterE">E</span></p> </div>"""

    from tests.utils import fix_bs4_parsing_spaces, compare_results
    a = fix_bs4_parsing_spaces(annotated)
    b = fix_bs4_parsing_spaces(expected)
    # compare_results(a, b)
    assert a == b
