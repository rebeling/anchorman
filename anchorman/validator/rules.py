# -*- coding: utf-8 -*-


def data_value(item, key):
    """Value of a specific key in item data."""
    return attributes_of(item).get(key)


def attributes_of(item):
    """Access intervall item data without knowing the key.

    item is an Interval(34, 37, ('fox', ('entity',
        {'fox': {'href': '/wiki/fox', 'type': 'animal'}})))

    :param item: intervaltree Interval
    :returns data: {'href': '/wiki/dog', 'type': 'animal'}
    """
    return item.data[1][1].values()[0]


def replacements_per_element(element, candidates, rules):
    """Replace only n elements of the same base element.

    A. Merkel, Mum Merkel, Mrs. Merkula - baseform *Angela Merkel*
    in most cases just marked once, but set value to as many times u want.
    """
    replaces_per_element = rules.get('replaces_per_element')
    extended_look_up_key = rules.get('replaces_per_element_extended_look_up')

    found = 0
    for candidate in candidates:
        if candidate.data[0] == element.data[0]:
            found += 1
        try:
            ka = attributes_of(element).get(extended_look_up_key)
            if ka:
                la = attributes_of(candidate).get(extended_look_up_key)
                if ka == la:
                    found += 1
        except:
            # ?! logging
            pass

        if found >= replaces_per_element:
            return False

    # if element.data[0] in existing_values:
    #     found += 1
    if found >= replaces_per_element:
        return False

    return True


def replacement_by_attribute(treeitem, unit_candidates, settings):
    """Check if already enough items with a specific attribute are in the
    candidates list for this unit.
    """
    replaces = settings.get('replaces')
    if replaces:
        items_per_unit = replaces['by_attribute'].get('value_per_unit')
        if items_per_unit:
            key = replaces['by_attribute']['key']
            attributes = [data_value(c, key) for c in unit_candidates]
            tree_item_key_value = data_value(treeitem, key)

            # ?! should we ignore this or tell the user
            # because None is just counting
            # if tree_item_key_value is None:
            #     raise AttributeError

            if tree_item_key_value:
                if attributes.count(tree_item_key_value) >= items_per_unit:
                    return False

    return True


def n_times_value_x_at_all(item, candidates, settings):
    """"""
    replaces = settings.get('replaces')
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


def filter_by_attribute(element, rules):
    """"""
    attributes = attributes_of(element)
    for key, val in rules['filter_by_attribute']['attributes']:
        if val == attributes.get(key):
            return False
    return True


def test_replacement_by_attribute():
    """"""
    from intervaltree import Interval
    item = Interval(65, 68, ('dog', (
        'entity', {
            'dog': {
                'score': 12.0, 'type': 'animal', 'value': '/wiki/dog'
            }
        })))

    settings = {
        'replaces': {
            'by_attribute': {
                'key': 'type',
                'value_per_unit': 1
            }
        }
    }

    assert replacement_by_attribute(item, [], {}) is True
    assert replacement_by_attribute(item, [], settings) is True
    assert replacement_by_attribute(item, [item], settings) is False

    settings['replaces']['by_attribute']['value_per_unit'] = 2
    assert replacement_by_attribute(item, [item, item], settings) is False


test_replacement_by_attribute()
