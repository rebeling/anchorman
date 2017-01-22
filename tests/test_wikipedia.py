# -*- coding: utf-8 -*-
from anchorman import annotate, get_config
from anchorman.utils import timeit


@timeit
def test_wiki_linking():

    from data.wiki_links import links
    with open('tests/data/wikibody_unlinked.html') as f:
        text = f.read()

    cfg = get_config()
    cfg['markup']['attributes'] = {
        "class": "anchorman",
        "data-entity": "link"
    }
    annotated = annotate(text, links, config=cfg)
    print len(links)

    # get rest and check
    assert annotated.count('class="anchorman"') == 711

    content = open('tests/data/index.tmpl', 'r').read()
    open('tests/data/wikipedia_annotated.html', 'w').write(content + annotated)
