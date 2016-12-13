# -*- coding: utf-8 -*-
from anchorman.generator.element import create_element_pattern, create_element
from anchorman.generator.unit import elements_of_unit


def n_times_value_overall(item, candidates, settings):

    replaces = settings.get('replaces')
    if replaces:
        key = replaces['by_attribute']['key']
        items_overall = replaces['by_attribute'].get('value_overall')
        if items_overall:
            all_for_now = 0
            for candidate in candidates:
                value = data_value(item, key)
                if value == key:
                    all_for_now += 1
                    if all_for_now >= items_overall:
                        return False

    return True


def specific_replace_rules(item, unit_candidates, settings):
    """Check item for specific replacement rules."""

    replaces = settings.get('replaces')
    if replaces:
        key = replaces['by_attribute']['key']
        items_per_unit = replaces['by_attribute'].get('value_per_unit')
        if items_per_unit:
            value = data_value(item, key)
            attributes = [data_value(c, key) for c in unit_candidates]
            if attributes.count(value) >= items_per_unit:
                return False

    return True


def data_value(item, key):
    """Value of a specific key in item data."""
    return attributes_of(item).get(key)


def attributes_of(item):
    """Access intervall item data without knowing the key.

    :param item: Interval(34, 37, ('fox', ('entity', {'fox': {'href': '/wiki/fox', 'type': 'animal'}})))
    :returns data: {'href': '/wiki/dog', 'type': 'animal'}
    """
    return item.data[1][1].values()[0]
