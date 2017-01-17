# -*- coding: utf-8 -*-
from anchorman.validator.rules import replacement_by_attribute
from anchorman.validator.rules import n_times_value_x_at_all
from anchorman.validator.rules import filter_by_attribute
from anchorman.validator.rules import replacements_per_element


def valid(element, candidates, unit_candidates, rules, own_validator):
    """Apply the rules specified in settings to the element.

    Take care of candidates already validated and the elements already
    added to this_unit.

    :param element:
    :param candidates:
    :param unit_candidates:
    :param rules:
    :param own_validator:
    """
    token, attributes = element

    # 2.1 replaces_per_element
    # add an entity as often as specified with replaces_per_element
    if rules.get('replaces_per_element'):
        if replacements_per_element(element, candidates, rules) is False:
            return False

    # 3. replaces_by_attribute per unit
    if rules.get('replaces'):
        if replacement_by_attribute(attributes, unit_candidates, rules) is False:
            return False
        # 3.1
        if n_times_value_x_at_all(attributes, candidates, rules) is False:
            return False

    # 4. filter_by_attribute
    if rules.get('filter_by_attribute'):
        if filter_by_attribute(element, rules) is False:
            return False

    # 5. create your own validator based on value or structure of element
    # to filter candidates out
    if own_validator:
        for validator in own_validator:
            if validator(element, candidates, unit_candidates, rules) is False:
                return False

    # element is valid
    return True
