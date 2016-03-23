# -*- coding: utf-8 -*-
from anchorman.generator.element import create_element_pattern, create_element
from anchorman.generator.unit import elements_of_unit


def specific_replace_rules(item, unit_candidates, settings):
    """Check item for specific replacement rules."""

    replaces = settings.get('replaces')
    if replaces:
        key = replaces['by_attribute']['key']
        items_per_unit = replaces['by_attribute']['type_per_unit']
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
