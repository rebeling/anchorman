# -*- coding: utf-8 -*-
from utils import fix_bs4_parsing_spaces
from tests.data.dummy import LINKS


def test_anchor_format():
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

    from anchorman import elements
    def my_format_element(a, b, c):
        return "RUMBLE"

    import copy

    newobj = copy.copy(elements.format_element)

    elements.format_element = my_format_element

    from anchorman import annotate, clean, get_config

    cfg = get_config()
    cfg['settings']['return_applied_links'] = True

    number_of_links_to_apply = 5
    cfg['rules']['replaces_at_all'] = number_of_links_to_apply
    cfg['markup']['decorate'] = {
        'tag': 'span'
    }

    annotated, applied, rest = annotate(RTEXT, RLINKS, config=cfg)
    assert len(applied) == number_of_links_to_apply

    expected = """<div>
    <p id="1">lala RUMBLE la lala RUMBLE RUMBLE RUMBLE la RUMBLE lalala RUMBLE RUMBLE RUMBLE</p>
    <p id="2">la RUMBLE RUMBLE RUMBLE lal RUMBLE RUMBLE la la RUMBLE la RUMBLE RUMBLE lala RUMBLE la</p>
    <p id="3">RUMBLE la RUMBLE RUMBLE RUMBLE la RUMBLE RUMBLE la RUMBLE RUMBLE lala RUMBLE RUMBLE la RUMBLE RUMBLE</p>
    </div>"""

    from utils import fix_bs4_parsing_spaces, compare_results
    a = fix_bs4_parsing_spaces(annotated)
    b = fix_bs4_parsing_spaces(expected)
    # compare_results(a, b)
    assert a == b

    elements.format_element = newobj
