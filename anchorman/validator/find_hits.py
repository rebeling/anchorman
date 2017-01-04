# -*- coding: utf-8 -*-
from anchorman.generator.element import create_element_pattern, create_element
from anchorman.validator.candidate import validate


def applicables(units, element_tree, config, own_validator):
    """Loop the units and validate each item in a unit.

    :param intervaltree:
    :param units:
    :param config:
    :param own_validator:
    """
    rules = config['rules']
    replaces_at_all = rules.get('replaces_at_all')

    candidates, to_be_applied = [], []
    for unit, (begin, end), _type in units:

        # # 1. replaces_at_all
        if replaces_at_all:
            if len(candidates) >= replaces_at_all:
                break

        unit_candidates = []
        for t_element in element_tree[begin:end]:
            # # check the rules

            # # 1. replaces_at_all
            if replaces_at_all:
                if len(candidates) >= replaces_at_all:
                    break

            element = t_element.data
            valid = validate(element,
                             candidates,
                             unit_candidates,
                             rules,
                             own_validator)

            if valid:
                element_str = create_element(t_element, config)
                to_be_applied.append((t_element, element_str))

                candidates.append(t_element)
                unit_candidates.append(t_element)

                # # 2. text_unit > number_of_items
                if len(unit_candidates) == rules.get('items_per_unit'):
                    break

    return to_be_applied
