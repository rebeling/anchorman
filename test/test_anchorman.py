#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import anchorman


text = (
    """<p>Foxes are small-to-medium-sized, omnivorous mammals belonging to several genera of the Canidae family. Foxes are slightly smaller than a medium-size domestic dog, with a flattened skull, upright triangular ears,<br> a pointed, slightly upturned snout, and a long bushy tail (or brush).</p>
    <p>Twelve species belong to the monophyletic group of Vulpes genus of "true foxes". Approximately another 25 current or extinct species are always or sometimes called foxes; these foxes are either part of the paraphyletic group of the South American foxes and the outlying group, which consists of Bat-eared fox, Gray fox, and Island fox.[1] Foxes are found on every continent except Antarctica. By far the most common and widespread <b>species</b> of fox is the red fox <i>(Vulpes vulpes)</i> with about 47 recognized sub-species.[2] The global distribution of foxes, together with their widespread reputation for cunning, has contributed to their prominence in popular culture and folklore in many societies around the world. The hunting of foxes with packs of hounds, long an established pursuit in Europe, especially in the British Isles, was exported by European settlers to various parts of the New World.</p>"""
    )


markup_format = {
    'tag': 'a',
    'value_key': 'href',
    'attributes': [
        ('class', 'anchorman')
        ],
    'rm-identifier': 'anchorman-link',
    }

markup_format2 = {
    'rm-identifier': 'anchorman-marker',
    'case-sensitive': False,
    'highlighting': {
        'pre': '${{',
        'post': '}}'
        }
    }


def test_anchorman_class(tmpdir):

    links = [
        {'Fox': {'value': '/fox'}},
        {'mammals': {'value': '/mammals'}},
        {'red fox': {
            'value': '/redfox',
            'attributes': [
                ('class', 'animal'),
                ('style', 'font-size:23px;background:red'),
                ('title', 'Fix und Foxi')
                ]
            }
        }
    ]

    a = anchorman.add(
        text,
        links,
        markup_format=markup_format, # default: a, href=value, class="anchorman"
        replaces_per_item=1          # default: all occurences
        )

    expected_replacement = '<a href="/mammals" class="anchorman" data-rm-key="anchorman-link">mammals</a>'
    expected_replacement2 = '<a href="/redfox" class="anchorman animal" data-rm-key="anchorman-link" style="font-size:23px;background:red" title="Fix und Foxi">red fox</a>'
    assert expected_replacement in a.result
    assert expected_replacement2 in a.result

    expected_counts = [('mammals', 1), ('red fox', 1), ('Fox', 0)]
    assert expected_counts == a.counts


    markup_items = [{'tail': {}}]
    a.add(
        a.result,
        markup_items,
        markup_format=markup_format2 # default: a, href=value, class="anchorman"
        )
    assert '${{tail}}' in a.result
    assert a.counts == [('tail', 1)]

    # remove the new markup
    a.remove()
    # remove the old links also
    a.remove(markup_format=markup_format)

    assert text.replace('<br>', '<br/>') == a.result

    assert a.__str__() == a.result
