# -*- coding: utf-8 -*-

p_text = '<p class="first">The qüick brown fox jumps</p> <p>over the lazy dog in Los Angeles.</p>'


t_text = 'The qüick brown fox jumps over the lazy dog in Los Angeles.'


elements = [
    {'qüick': {
        'value': '/wiki/queick',
        'score': 0.2,
        'type': 'term'}},
    {'fox': {
        'value': '/wiki/fox',
        'score': 23.0,
        'type': 'animal'}},
    {'lazy': {
        'value': '/wiki/lazy',
        'score': 5.55,
        'type': 'term'}},
    {'dog': {
        'value': '/wiki/dog',
        'score': 12.0,
        'type': 'animal'}},
    {'Los Angeles': {
        'value': '/wiki/los-angeles',
        'score': 42.0,
        'type': 'city'}}
    ]

