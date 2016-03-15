# -*- coding: utf-8 -*-
from copy import copy
from bs4 import BeautifulSoup


def augment_bs4tag(bs4tag, item, tag_markup, original):
    """Fill the base bs4tag element with data of the item."""

    tag = copy(bs4tag)

    # add the attribute value pairs of item
    exclude_keys = tag_markup.get('exclude_keys', [])
    for key, value in item.values()[0].items():
        if key not in exclude_keys:
            tag[key] = value

    # add the text
    tag.string = original

    return tag


def create_bs4tag(markup):
    """Use BeautifulSoup to create a base tag element."""

    tag = markup['tag']
    attributes = markup.get('attributes', {})

    return BeautifulSoup("", "lxml").new_tag(tag, **attributes)
