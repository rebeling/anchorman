#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree, html


def to_tree(s):
    xml = "<root> %s </root>" % s
    return etree.fromstring(xml)


def from_tree(tree):
    return etree.tounicode(tree)[6:-7].strip()
