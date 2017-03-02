# -*- coding: utf-8 -*-
from anchorman import annotate, clean, get_config
import re

    # generalize!


def test_annotate_settings():

    TEXT = """<div><p>Paris Hilton wasn't going to let a bit of snowfall ruin her trip to New York City.</p><p>The Stars Are Blind singer, who was born in the Big Apple, was snapped Friday boarding a vehicle amid snowy conditions to check out the on-goings as fashion fever overtakes the city that never sleeps for New York Fashion Week.</p><p>The 35-year-old socialite matched well with a black and red leather jacket in Paris.</p></div>"""

    RESULT = """<div><p>Paris Hilton wasn\'t going to let a bit of snowfall ruin her trip to New York City.</p><p>The Stars Are Blind singer, who was born in the Big Apple, was snapped Friday boarding a vehicle amid snowy conditions to check out the on-goings as fashion fever overtakes the city that never sleeps for New York Fashion Week.</p><p>The 35-year-old socialite matched well with a black and red leather jacket in <a class="anchorman" lemma="Paris" type="location">Paris</a>.</p></div>"""


    links = [
        {u'Paris': {
            'lemma': u'Paris', 'type': 'location'}},
        {u'Paris Hilton': {
            'lemma': u'Paris Hilton', 'type': 'person'}}
    ]


    cfg = get_config()

    cfg['markup'] = {
        'anchor_pattern': '<a class="anchorman" lemma="{lemma}" type="{type}">{token}</a>',
        'decorate_anchor_key': 'the_anchor'
    }    

    rules = {
        'return_applied_links': True,
        # apply high score candidates first
        'sort_by_item_value': {
            'key': 'score',
            'default': 0
        },
        # 'replaces_per_element': {
        #     'number': 1,
        #     'key': 'lemma'
        # },
        # 'replaces_at_all': 5, #self.max_links,
        # not available 'longest_match_first': False,
        # 'replaces': {
        #     'by_attribute': {
        #         'key': 'type',
        #         # 'value_per_unit': 1
        #         'value_overall': 2 #self.max_per_etype
        #     }
        # },
        'items_per_unit': 4, #self.links_per_paragraph,


        'filter_by_attribute': {
            'attributes':[
                {'key': 'type', 'value': 'person'}
            ]
        }
    }

    settings = {
        # "log_level": "DEBUG",
        "return_applied_links": True,
        # "forbidden_areas": {
        #     "tags": ["img", "a"],
            # "classes": ["first", "p--heading-3"]
        # }
    }

    cfg['settings'].update(settings)
    cfg['rules'].update(rules)

    annotated, applied, rest = annotate(TEXT, links, config=cfg)

    from tests.utils import compare_results

    RESULT = re.sub(" +", " ", RESULT)
    compare_results(annotated, RESULT)
    assert annotated == RESULT
