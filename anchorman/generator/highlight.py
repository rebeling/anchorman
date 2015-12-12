# -*- coding: utf-8 -*-
from copy import copy


def augment_highlight(highlight, item): #, highlight_markup):
    """Fill the base highlight element with data of the item."""

    string = copy(highlight)

    # add the text
    item_key = item.keys()[0]
    string = string.format(item_key)

    return string


def create_highlight(highlight_markup):
    """Use format to create a base highlight element."""

    highlight = highlight_markup['pre'] + "{}" + highlight_markup['post']

    return highlight
