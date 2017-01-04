# -*- coding: utf-8 -*-
from copy import copy


def augment_highlight(highlight, original):
    """Fill the base highlight element with data of the item.

    The string manipulation with format causes problems on template
    syntax with curly brackets.
    :param highlight:
    :param original:
    """
    string = copy(highlight)
    string = string % original

    return string


def create_highlight(highlight_markup):
    """Use format to create a base highlight element.

    :param highlight_markup:
    """
    highlight = highlight_markup['pre'] + "%s" + highlight_markup['post']

    return highlight
