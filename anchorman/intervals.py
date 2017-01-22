# -*- coding: utf-8 -*-
from anchorman.elements import element_slices, elements_per_unit
from anchorman.units import unit_slices, units_gen
from anchorman.utils import soup_it


def all_intervals(text, elements, config):
    """From the slices of elements and units create an intervaltree.

    time consuming and may unnessesary to search the whole txt
    1. search all elements in text
    2. search all elements in paragraph!
    3. links > 40: search with aho-coressio search algo for speed
       500 links take 10 seconds

    :param text:
    :param elements:
    :param config:
    """
    settings = config['settings']
    rules = config['rules']
    the_soup = soup_it(text, settings)

    units, forbidden = unit_slices(text, the_soup, settings)
    # What if I have the positions already
    # do they align with ...not after the parsing for units.
    unit_elements_gen = elements_per_unit(
        units, forbidden, element_slices(the_soup[1], elements, rules))

    old_links = {token: (f, t) for f, t, token in forbidden if token}

    return unit_elements_gen, old_links, the_soup[1]
