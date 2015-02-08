#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree, html


def to_tree(string):
    string = "<root>%s</root>" % string
    try:
        return etree.fromstring(string)
    except:
        return html.fromstring(string)

def from_tree(tree):
    return etree.tounicode(tree)[6:-7].strip()
