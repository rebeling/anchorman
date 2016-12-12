# -*- coding: utf-8 -*-
from anchorman.generator.candidate_utils import (
    specific_replace_rules, attributes_of)
from anchorman.generator.element import (
    create_element_pattern, create_element)
from anchorman.generator.unit import elements_of_unit


def validate(item, candidates, unit_candidates, settings, own_validator):
    """Apply the rules specified in settings to the item.

    Take care of candidates already validated and the items already
    added to this_unit.

    :param item:
    :param candidates:
    :param this_unit:
    :param settings:
    :param own_validator:

    .. todo::
        check context of replacement: do not add links in links, or inline of overlapping elements, ...
        replace only one item of an entity > e.g. A. Merkel, Mum Merkel, ...

    """
    # print 'validate', item, candidates, settings, this_unit
    # print candidates
    # replaces_per_item = True
    # check if an item like this same token wsa set already?!
    # replaces_per_type = settings.get('replaces_per_item')
    # if replaces_per_type:
    #     if candidates.count(item) >= replaces_per_type:
    #         return False

    # 0. check if the context is ok for replacement
    

    # 1. replaces_at_all
    replaces_at_all = settings.get('replaces_at_all')
    if isinstance(replaces_at_all, int) and replaces_at_all <= len(candidates):
        return False

    # 2. text_unit > number_of_items
    items_per_unit = settings.get('text_unit', {}).get('items_per_unit')
    if isinstance(items_per_unit, int) and items_per_unit <= len(unit_candidates):
        return False

    # 2.1 replaces_per_item
    # add entity as often as specified with replaces_per_item
    replaces_per_item = settings.get('replaces_per_item', None)
    if replaces_per_item:
        found = 0
        for candidate in candidates:
            if candidate.data[0] == item.data[0]:
                found += 1
            if found >= replaces_per_item:
                return False

    # 3. replaces_by_attribute
    if specific_replace_rules(item, unit_candidates, settings) is False:
        return False

    # 4. filter_by_attribute
    filter_by_attribute = settings.get('filter_by_attribute')
    if filter_by_attribute:
        attributes = attributes_of(item)
        for key, val in filter_by_attribute['attributes']:
            if val == attributes.get(key):
                return False

    # 5. create your own validator based on value or structure of item
    # to filter candidates out - create a list of types like candidates
    if own_validator:
        for validator in own_validator:
            if validator(item, candidates, unit_candidates, settings) is False:
                return False

    # item is valid
    return True


def retrieve_hits(intervaltree, units, config, own_validator):
    """Loop the units and validate each item in unit.

    :param intervaltree:
    :param units:
    :param config:
    :param own_validator:
    """

    settings = config['settings']
    mode = settings['mode']
    markup = config['markup']
    element_pattern = create_element_pattern(mode, markup)

    candidates = []
    to_be_applied = []
    for unit in sorted(units):

        unit_candidates = []
        for item in elements_of_unit(intervaltree, unit, settings):

            valid = validate(item, candidates, unit_candidates, settings,
                             own_validator)
            if valid:
                element = create_element(element_pattern, item, mode, markup)
                to_be_applied.append((item, element))
                candidates.append(item)
                unit_candidates.append(item)

    return to_be_applied
