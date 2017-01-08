# -*- coding: utf-8 -*-
from anchorman.generator.element import create_element_pattern, create_element
from anchorman.validator import candidate


def applicables(units, element_tree, config, own_validator):
    """Loop the units and validate each item in a unit.

    :param units:
    :param element_tree:
    :param config:
    :param own_validator:
    """
    rules = config['rules']
    replaces_at_all = rules.get('replaces_at_all')
    items_per_unit = rules.get('items_per_unit')

    candidates = []
    for unit, (begin, end), _type in units:

        # # 1. replaces_at_all
        if replaces_at_all and len(candidates) >= replaces_at_all:
            break

        unit_candidates = []
        for t_element in element_tree[begin:end]:
            # # check the rules
            # # 1. replaces_at_all
            if replaces_at_all and len(candidates) >= replaces_at_all:
                break

            if candidate.valid(t_element, candidates, unit_candidates, rules,
                               own_validator):
                candidates.append(t_element)
                unit_candidates.append(t_element)

                # # 2. text_unit > number_of_items
                if items_per_unit and len(unit_candidates) == items_per_unit:
                    break

    return [(c, create_element(c, config)) for c in candidates]
