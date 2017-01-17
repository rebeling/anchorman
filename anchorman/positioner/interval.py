# -*- coding: utf-8 -*-
from anchorman.positioner.slices import unit_slices, element_slices


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
    units, forbidden = unit_slices(text, config)
    unit_elements = elements_per_units(
        units, forbidden, element_slices(text, elements, config))

    return units, unit_elements


def elements_per_units(units, forbidden, data):
    """Create an intervaltree for units and forbidden.

    :param forbidden:
    :param data:
    """
    lookup = set([x for f, t in forbidden for x in range(f, t)])
    for _from, _to in units:
        yield [(t_from, t_to, token, element)
               for t_from, t_to, token, element in data
               if t_from not in lookup and t_to not in lookup
               # check if element fits the unit
               if _from < t_from and t_to < _to]
