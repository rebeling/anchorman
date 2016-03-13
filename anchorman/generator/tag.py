# -*- coding: utf-8 -*-
from copy import copy
from bs4 import BeautifulSoup


def augment_bs4tag(bs4tag, item, tag_markup, original):
    """Fill the base bs4tag element with data of the item."""

    tag = copy(bs4tag)

    # add the attribute value pairs of item
    item_values = item.values()[0]
    exclude_keys = tag_markup.get('exclude_keys', [])

    for key, value in item_values.items():

        if key not in exclude_keys:
            tag[key] = value

    # add the text
    tag.string = original

    return tag


def create_bs4tag(tag_markup):
    """Use BeautifulSoup to create a base tag element."""

    new_soup = BeautifulSoup("", "lxml")

    kwargs = {}
    for attr_value in tag_markup.get('attributes', []):
        attribute_value = attr_value.split(' ')
        kwargs[attribute_value[0]] = ' '.join(attribute_value[1:])

    bs4tag = new_soup.new_tag(tag_markup['tag'], **kwargs)

    return bs4tag
