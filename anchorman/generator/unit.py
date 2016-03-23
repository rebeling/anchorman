# -*- coding: utf-8 -*-


def elements_of_unit(intervaltree, unit, settings):
    """Get all items / elements of the actual unit to validate.

    :param intervaltree:
    :param unit:
    :param settings:
    """

    element_identifier = settings['element_identifier']
    subtree = intervaltree[unit.begin:unit.end]

    test_items = [item
                  for item in sorted(subtree)
                  if item.data[1][0] == element_identifier]

    return test_items
