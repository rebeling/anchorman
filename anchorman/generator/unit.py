# -*- coding: utf-8 -*-


def elements_of_unit(intervaltree, unit, settings):
    """Get all items / elements of the actual unit to validate.

    :param intervaltree:
    :param unit:
    :param settings:
    """

    element_identifier = settings['element_identifier']
    subtree = intervaltree[unit.begin:unit.end]
    sort_by_item_value = settings.get('sort_by_item_value')

    if sort_by_item_value:
        key = sort_by_item_value['key']
        default = sort_by_item_value.get('key', 0)
        test_items = [(item.data[1][1].values()[0].get(key, default), item)
                      for item in sorted(subtree)
                      if item.data[1][0] == element_identifier]
        test_items.sort(key=lambda tup: tup[0], reverse=True)
        test_items = [y for x, y in test_items]
    else:
        test_items = [item
                      for item in sorted(subtree)
                      if item.data[1][0] == element_identifier]

    return test_items
