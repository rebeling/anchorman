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
    </div>"""

    cfg = get_config()
    cfg['settings']['return_applied_links'] = True

    number_of_links_to_apply = 5
    cfg['rules']['replaces_at_all'] = number_of_links_to_apply
    cfg['markup']['rest'] = {
        'tag': 'span'
    }

    annotated, applied, rest = annotate(RTEXT, RLINKS, config=cfg)
    assert len(applied) == number_of_links_to_apply

    expected = """<div>
    <p id="1">lala <a class="anchorman" score="42" type="letterA">A</a> la lala <a class="anchorman" score="42" type="letterA">AA</a> <a class="anchorman" score="42" type="letterB">BB</a> <a class="anchorman" score="42" type="letterB">B</a> la <a class="anchorman" score="42" type="letterC">C</a> lalala <span score="42" type="letterD">DDD</span> <span score="42" type="letterD">D</span> <span score="42" type="letterE">E</span></p>
    <p id="2">la <span score="42" type="letterE">E</span> <span score="42" type="letterE">EE</span> <span score="42" type="letterA">AA</span> lal <span score="42" type="letterC">CC</span> <span score="42" type="letterC">C</span> la la <span score="42" type="letterB">BB</span> la <span score="42" type="letterD">DD</span> <span score="42" type="letterD">D</span> lala <span score="42" type="letterE">EE</span> la</p>
    <p id="3"><span score="42" type="letterB">B</span> la <span score="42" type="letterB">BB</span> <span score="42" type="letterE">EEE</span> <span score="42" type="letterA">A</span> la <span score="42" type="letterC">CCC</span> <span score="42" type="letterB">B</span> la <span score="42" type="letterD">DDD</span> <span score="42" type="letterC">C</span> lala <span score="42" type="letterA">AAA</span> <span score="42" type="letterD">D</span> la <span score="42" type="letterB">BBB</span> <span score="42" type="letterE">E</span></p>
    </div>"""

    from utils import fix_bs4_parsing_spaces, compare_results
    a = fix_bs4_parsing_spaces(annotated)
    b = fix_bs4_parsing_spaces(expected)
    # compare_results(a, b)
    assert a == b
