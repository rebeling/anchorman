# -*- coding: utf-8 -*-

p_text = '<p class="first">The qüick brown fox jumps</p> <p>over the lazy dog in Los Angeles.</p>'


t_text = 'The qüick brown fox jumps over the lazy dog in Los Angeles.'

s_text = 'Angela Merkel, CDU, Bundeskanzlerin'

s1_elements = [
    {"Angela Merkel, CDU, Bundeskanzlerin": {
        'itemtype': 'http://schema.org/Person',
        'itemscope': None}},
    ]

s11_elements = [
    {"CDU": {
        'itemtype': 'http://schema.org/Organization',
        'itemscope': None}},
    ]

s2_elements = [
    {"Angela Merkel": {'itemprop': 'name'}},
    {"CDU": {'itemprop': 'name'}},
    {"Bundeskanzlerin": {'itemprop': 'jobtitle'}}
    ]





    # {'fox': {
    #     'href': '/wiki/fox',
    #     'score': 23.0,
    #     'type': 'animal',
    #     'itemscope': None}}, <<< !


elements = [
    {'qüick': {
        'href': '/wiki/queick',
        'score': 0.2,
        'type': 'term'}},
    {'fox': {
        'href': '/wiki/fox',
        'score': 23.0,
        'type': 'animal'}},
    {'lazy': {
        'href': '/wiki/lazy',
        'score': 5.55,
        'type': 'term'}},
    {'dog': {
        'href': '/wiki/dog',
        'score': 12.0,
        'type': 'animal'}},
    {'Los Angeles': {
        'href': '/wiki/los-angeles',
        'score': 42.0,
        'type': 'city'}}
    ]

