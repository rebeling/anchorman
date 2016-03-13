# -*- coding: utf-8 -*-
from .element import create_element_pattern, create_element


def data_val(item, replaces_per_attribute):
    """Get the item.data """
    idata = item.data[1][1].values()[0]
    rpa = replaces_per_attribute
    return idata.get(rpa['attribute_key']) if rpa else idata


def validate(item, candidates, this_unit, setting, own_validator):
    """Apply the rules specified in setting to the item.

    Take care of candidates already validated and the items already
    added to this_unit.

    .. todo::
        check context of replacement: do not add links in links, or inline of overlapping elements, ...
        replace only one item of an entity > e.g. A. Merkel, Mum Merkel, ...
    """
    # print 'validate', item, candidates, setting, this_unit

    # replaces_per_item = True
    # check if an item like this same token wsa set already?!
    # replaces_per_type = setting.get('replaces_per_item')
    # if replaces_per_type:
    #     if candidates.count(item) >= replaces_per_type:
    #         return False

    # use a specific value of link structure to filter here
    # must be list of types like candidates
    if own_validator:
        for validator in own_validator:
            valid = validator(item, candidates, this_unit, setting)
            if valid is False:
                return False

    # replaces_per_attribute
    replaces_per_attribute = setting.get('replaces_per_attribute')
    if replaces_per_attribute:
        value = data_val(item, replaces_per_attribute)
        number_of_items = replaces_per_attribute['number_of_items']
        attributes = [data_val(x, replaces_per_attribute) for x in candidates]
        if attributes.count(value) >= number_of_items:
            return False

    # replaces_at_all
    replaces_at_all = setting.get('replaces_at_all')
    if isinstance(replaces_at_all, int) and len(candidates) >= replaces_at_all:
        return False

    # text_unit > number_of_items
    items_per_unit = setting.get('text_unit', {}).get('number_of_items')
    if isinstance(items_per_unit, int) and items_per_unit <= len(this_unit):
        return False

    # filter_by_value
    filter_by_value = setting.get('filter_by_value')
    if filter_by_value:
        values = data_val(item, None)
        for key, val in filter_by_value.items():
            if val > values[key]:
                return False

    # item is valid
    return True


def elements_of_unit(intervaltree, unit, setting):
    """Get all items / elements of the actual unit to validate."""

    element_identifier = setting['element_identifier']
    subtree = intervaltree[unit.begin:unit.end]
    test_items = []
    for item in sorted(subtree):
        if item.data[1][0] == element_identifier:
            test_items.append(item)
    return test_items


def retrieve_hits(intervaltree, units, config, own_validator):
    """Loop the units and validate each item in unit."""

    setting = config['setting']
    mode = setting['mode']
    markup = config['markup']
    element_pattern = create_element_pattern(mode, markup)

    candidates = []
    to_be_applied = []
    for unit in sorted(units):

        this_unit = []
        for item in elements_of_unit(intervaltree, unit, setting):

            valid = validate(item, candidates, this_unit, setting, own_validator)
            if valid:
                element = create_element(element_pattern, item, mode, markup)
                to_be_applied.append((item, element))
                candidates.append(item)
                this_unit.append(item)

    return to_be_applied
