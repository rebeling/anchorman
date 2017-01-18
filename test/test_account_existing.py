# -*- coding: utf-8 -*-
from anchorman import annotate, clean, get_config
from utils import fix_bs4_parsing_spaces


def test_context_awareness():
    """Test annotate elements with default and manipulated config."""

    text = """<p>Intel analysis shows <a href="/oldlink">Vladimir Putin</a> approved election hacking Vladimir Putin.</p>"""

    links = [
        {
            "Vladimir Putin": {
                "href": "/putin", "type": "person", "score": 100.42
            }
        },
        {
            "Putin": {
                "href": "/putin", "type": "person", "score": 100.42
            }
        }
    ]

    cfg = get_config()
    cfg['settings']['log_level'] = 'DEBUG'

    # use default settings
    annotated = annotate(text, links, config=cfg)
    expected = """<p>Intel analysis shows <a href="/oldlink">Vladimir Putin</a> approved election hacking <a class="anchorman" href="/putin" score="100.42" type="person">Vladimir Putin</a>.</p>"""

    assert annotated == expected

    cfg['rules']['replaces_per_element'] = {"number": 1, "key": "href"}
    annotated = annotate(text, links, config=cfg)
    expected2 = """<p>Intel analysis shows <a href="/oldlink">Vladimir Putin</a> approved election hacking Vladimir Putin.</p>"""

    assert annotated == expected2
