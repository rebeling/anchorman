# -*- coding: utf-8 -*-
from intervaltree import IntervalTree
from anchorman.positioner.slices import element_slices, unit_slices


def to_intervaltree(data, t=None):
    """Create an intervaltree of all elements (elements, units, ...)."""

    if t is None:
        t = IntervalTree()

    for token, slices, _type in data:
        _from, _to = slices
        t[_from:_to] = (token, _type)

    return t


def unit_intervals(intervaltree, text_unit):
    """Loop the intervaltree to get the text unit interval items."""

    text_unit_key_name = text_unit['key'], text_unit['name']

    units = []
    for item in intervaltree.items():
        interval_key_name = item.data[0], item.data[1][0]
        if interval_key_name == text_unit_key_name:
            units.append(item)

    return units


def intervals(text, elements, setting):
    """From the slices of elements and units create an intervaltree."""

    text_unit = setting['text_unit']

    slices = element_slices(text, elements, setting)
    text_units = unit_slices(text, text_unit)
    slices.extend(text_units)

    intervaltree = to_intervaltree(slices)
    text_unit_intervals = unit_intervals(intervaltree, text_unit)

    return intervaltree, text_unit_intervals
