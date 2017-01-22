# -*- coding: utf-8 -*-
from anchorman.utils import log, timeit


@timeit
def valid(element, candidates, unit_candidates, rules, old_links,
          own_validator):
    """Apply the rules specified in settings to the element.

    Take care of candidates already validated and the elements already
    added to this_unit.

    :param element:
    :param candidates:
    :param unit_candidates:
    :param rules:
    :param own_validator:
    """
    # 2.1 replaces_per_element
    # add an entity as often as specified with replaces_per_element
    # if rules.get('replaces_per_element'):
    #     if replacements_per_element(
    #             element, candidates, rules, old_links) is False:
    #         return False

    args = (element, candidates, unit_candidates, rules, old_links)

    if replaces_per_element(*args) is False:
        return False

    # 3. replaces_by_attribute per unit
    if replaces_by_attribute(*args) is False:
        return False

    # 3.1
    if n_times_key_value(*args) is False:
        return False

    # 4. filter_by_attribute
    if filter_by_attribute(*args) is False:
        return False

    # # 5. create your own validator based on value or structure of element
    # # to filter candidates out
    # if own_validator:
    #     for validator in own_validator:
    #         if validator(*args) is False:
    #             return False

    # element is valid
    return True


def replaces_per_element(element, candidates, _x, rules, old_links):
    """Replace only n elements of the same base element.

    A. Merkel, Mum Merkel, Mrs. Merkula - baseform *Angela Merkel*
    in most cases just marked once, but set value to as many times u want.
    """
    if rules.get('replaces_per_element'):
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


def replaces_by_attribute(element, candidates, unit_candidates, rules, _x):
    """Check if already enough items with a specific attribute are in the
    candidates list for this unit.
    """
    if rules.get('replaces_by_attribute'):
        _, element_attributes = element
        replaces = rules.get('replaces_by_attribute')
        if replaces:
            items_per_unit = replaces.get('value_per_unit')
            if items_per_unit:
                key = replaces['key']
                attributes = [c[3].get(key) for c in unit_candidates]
                tree_item_key_value = element_attributes.get(key)
                # ?! should we ignore this or tell the user
                # because None is just counting
                # if tree_item_key_value is None:
                #     raise AttributeError
                if tree_item_key_value:
                    if attributes.count(tree_item_key_value) >= items_per_unit:
                        return False
    return True


def n_times_key_value(element, candidates, unit_candidates, rules, _x):
    """"""
    if rules.get('n_times_key_value'):
        _, element_attributes = element
        replaces = rules.get('n_times_key_value')
        key = replaces['key']
        items_overall = replaces.get('value_overall')

        if items_overall:
            all_for_now = 0
            value = element_attributes.get(key)

            for _, _, _, c_attr in candidates:
                if value == c_attr.get(key):
                    all_for_now += 1
                    if all_for_now >= items_overall:
                        return False
    return True


def filter_by_attribute(element, _x, _y, rules, _z):
    """"""
    if rules.get('filter_by_attribute'):
        _, element_attributes = element
        for key_val in rules['filter_by_attribute']['attributes']:
            kv = key_val.items()[0]
            if kv[1] == element_attributes.get(kv[0]):
                return False
    return True
