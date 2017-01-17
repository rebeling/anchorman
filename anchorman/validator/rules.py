# -*- coding: utf-8 -*-


def replacements_per_element(token, attributes, candidates, rules):
    """Replace only n elements of the same base element.

    A. Merkel, Mum Merkel, Mrs. Merkula - baseform *Angela Merkel*
    in most cases just marked once, but set value to as many times u want.
    """
    replaces_per_element = rules.get('replaces_per_element')
    extended_look_up_key = rules.get('replaces_per_element_extended_look_up')

    found = 0
    for _, _, candidate, candidate_attributes in candidates:
        if candidate == token:
            found += 1
        try:
            ka = attributes.get(extended_look_up_key)
            if ka:
                la = candidate_attributes.get(extended_look_up_key)
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

            attributes = [c.get(key) for c in unit_candidates]
            tree_item_key_value = treeitem.get(key)

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
            value = item.get(key)
            if value == key:
                all_for_now += 1
                if all_for_now >= items_overall:
                    return False
    return True


def filter_by_attribute(attributes, rules):
    """"""
    for key, val in rules['filter_by_attribute']['attributes']:
        if val == attributes.get(key):
            return False
    return True


# def test_replacement_by_attribute():
#     """"""
#     from intervaltree import Interval
#     item = Interval(65, 68, ('dog', (
#         'entity', {
#             'dog': {
#                 'score': 12.0, 'type': 'animal', 'value': '/wiki/dog'
#             }
#         })))

#     settings = {
#         'replaces': {
#             'by_attribute': {
#                 'key': 'type',
#                 'value_per_unit': 1
#             }
#         }
#     }

#     assert replacement_by_attribute(item, [], {}) is True
#     assert replacement_by_attribute(item, [], settings) is True
#     assert replacement_by_attribute(item, [item], settings) is False

#     settings['replaces']['by_attribute']['value_per_unit'] = 2
#     assert replacement_by_attribute(item, [item, item], settings) is False


# test_replacement_by_attribute()
