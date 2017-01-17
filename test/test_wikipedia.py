# -*- coding: utf-8 -*-
from anchorman import annotate, clean, get_config

def test_wiki_linking():

    from data.wiki_links import links
    with open('test/data/wikibody_unlinked.html') as f:
        text = f.read()
    # use default settings
    annotated = annotate(text, links)
    print len(links)

    # get rest and check
    assert annotated.count('class="anchorman"') == 591
