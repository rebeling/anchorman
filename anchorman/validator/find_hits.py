# -*- coding: utf-8 -*-
from anchorman.generator import create_element
from anchorman.validator import candidate


def applicables(units, elements_per_units, config, own_validator):
    """Loop the units and validate each item in a unit.

    :param units:
    :param elements_per_units:
    :param config:
    :param own_validator:
    """
    rules = config['rules']
    replaces_at_all = rules.get('replaces_at_all')
    items_per_unit = rules.get('items_per_unit')

    candidates = []
    for elements in elements_per_units:
        # # 1. replaces_at_all
        if replaces_at_all and len(candidates) >= replaces_at_all:
            break

        unit_candidates = []
        for _from, _to, token, element in elements:
            # # check the rules
            # # 1. replaces_at_all
            if replaces_at_all and len(candidates) >= replaces_at_all:
                break

            candito = (token, element)
            if candidate.valid(
                candito, candidates, unit_candidates, rules, own_validator):

                candidates.append((_from, _to, token, element))
                unit_candidates.append((_from, _to, token, element))

                # # 2. text_unit > number_of_items
                if items_per_unit and len(unit_candidates) == items_per_unit:
                    break

    anchors = [create_element(c, config) for c in candidates]
    return anchors
