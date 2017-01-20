# -*- coding: utf-8 -*-
from anchorman.positioner.slices import unit_slices, element_slices
from anchorman.utils import log


def intervals(text, elements, config):
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
    units, forbidden, soup_string = unit_slices(text, config)

    # What if I have the positions already
    # do they align with ...not after the parsing for units.

    unit_elements_gen = elements_per_units(
        units, forbidden, element_slices(soup_string, elements, config))

    old_links = linked_already(forbidden)

    return unit_elements_gen, old_links, soup_string


def linked_already(forbidden):
    return {token: (f, t) for f, t, token in forbidden if token}


def elements_per_units(units, forbidden, data):
    """Create an intervaltree for units and forbidden.

    :param forbidden:
    :param data:
    """
    lookup = {x for f, t, token in forbidden for x in range(f, t)}
    for _from, _to, string in units:
        yield ((_from, _to, string),
               [(t_from, t_to, token, element)
                for t_from, t_to, token, element in data
                if t_from not in lookup and t_to-1 not in lookup
                # check if element fits the unit
                if _from < t_from and t_to < _to])
