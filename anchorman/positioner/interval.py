# -*- coding: utf-8 -*-
from intervaltree import IntervalTree
from anchorman.positioner.slices import element_slices, unit_slices


def to_intervaltree(data, t=None):
    """Create an intervaltree of all elements (elements, units, ...).
    :param t:
    :param data:
    """

    if t is None:
        t = IntervalTree()

    overlaps = []
    existing_values = []
    existing_a_tags = []
    for token, slices, _type in data:
        _from, _to = slices
        t[_from:_to] = (token, _type)

        if _type[0] == 'restricted_area':
            overlaps.append((_from, _to, token, _type))
            a, b = token
            if a == 'a':
                existing_values.append(b)
                existing_a_tags.append((_from, _to))

    # remove all elements in restricted_areas
    if overlaps:
        for begin, end, token, _type in overlaps:
            t.remove_envelop(begin, end)

    return t, existing_values, existing_a_tags


def unit_intervals(intervaltree, text_unit):
    """Loop the intervaltree to get the text unit interval items.
    :param text_unit:
    :param intervaltree:
    """

    text_unit_key_name = text_unit['key'], text_unit['name']

    # add to units if interval_key_name == text_unit_key_name
    units = [item
             for item in intervaltree.items()
             if (item.data[0], item.data[1][0]) == text_unit_key_name]

    return units


def intervals(text, elements, settings):
    """From the slices of elements and units create an intervaltree.

    :param settings:
    :param elements:
    :param text:
    """
    text_unit = settings['text_unit']

    slices = element_slices(text, elements, settings)
    text_units = unit_slices(text,
                             text_unit['key'],
                             text_unit['name'],
                             text_unit.get('restricted_areas'))
    slices.extend(text_units)

    intervaltree, existing_values, existing_a_tags = to_intervaltree(slices)
    text_unit_intervals = unit_intervals(intervaltree, text_unit)

    return intervaltree, text_unit_intervals, existing_values, existing_a_tags
