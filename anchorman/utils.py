#!/usr/bin/env python
# -*- coding: utf-8 -*-

def sort_for_longest_match_first(links):
    keys = {x.keys()[0]:x for x in links}
    xs = sorted(keys.keys(), key=len, reverse=True)
    b = []
    append = b.append
    for y in xs:
        append(keys[y])
    return b
