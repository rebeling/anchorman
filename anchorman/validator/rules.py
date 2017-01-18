# -*- coding: utf-8 -*-
from anchorman.utils import log

def replacements_per_element(element, candidates, rules, old_links):
    """Replace only n elements of the same base element.

    A. Merkel, Mum Merkel, Mrs. Merkula - baseform *Angela Merkel*
    in most cases just marked once, but set value to as many times u want.
    """
    token, attributes = element
    replaces_per_element = rules.get('replaces_per_element')
    key = replaces_per_element['key']
    n = replaces_per_element['number']

    found = 0

    # do we really want this or better check items in links
    # based on attributes only
    if token in old_links:
        found += 1
        # return False

    for _, _, candidate, candidate_attributes in candidates:
        if candidate == token:
            found += 1
        try:
            ka = attributes.get(key)
            if ka:
                la = candidate_attributes.get(key)
                if ka == la:
                    found += 1
        except Exception as e:
            log("No such attributes: {}".format(attributes))

        if found >= n:
            return False

    if found >= n:
        return False

    return True


def replacement_by_attribute(element, unit_candidates, settings):
    """Check if already enough items with a specific attribute are in the
    candidates list for this unit.
    """
    _, element_attributes = element
    replaces = settings.get('replaces')
    if replaces:
        items_per_unit = replaces['by_attribute'].get('value_per_unit')
        if items_per_unit:
            key = replaces['by_attribute']['key']

            attributes = [c.get(key) for c in unit_candidates]
            tree_item_key_value = element_attributes.get(key)

            # ?! should we ignore this or tell the user
            # because None is just counting
            # if tree_item_key_value is None:
            #     raise AttributeError

            if tree_item_key_value:
                if attributes.count(tree_item_key_value) >= items_per_unit:
                    return False

    return True


def n_times_value_x_at_all(element, candidates, settings):
    """"""
    _, element_attributes = element
    replaces = settings.get('replaces')
    key = replaces['by_attribute']['key']
    items_overall = replaces['by_attribute'].get('value_overall')
    if items_overall:
        all_for_now = 0

        for candidate in candidates:
            value = element_attributes.get(key)
            if value == key:
                all_for_now += 1
                if all_for_now >= items_overall:
                    return False
    return True


def filter_by_attribute(element, rules):
    """"""
    _, element_attributes = element
    for key, val in rules['filter_by_attribute']['attributes']:
        if val == element_attributes.get(key):
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
