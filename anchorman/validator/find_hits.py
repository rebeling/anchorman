# -*- coding: utf-8 -*-
from anchorman.generator import create_element
from anchorman.validator import candidate
from anchorman.utils import log


def the_applicables(candidates, config):
    anchors = [create_element(c, config) for c in candidates]
    log("\nAnchors: \n  {}".format('\n  '.join([str(a) for a in anchors])))
    return anchors


def items_per_unit_satisfied(items_per_unit, unit_candidates, old_links, u_from, u_to):
    if items_per_unit:
        if len(unit_candidates) == items_per_unit:
            return True

        # check against the old_links in this unit
        if old_links:
            count_old_links = len(unit_candidates)
            for k, v in old_links.iteritems():
                _f, _t = v
                if u_from < _f and _t < u_to:
                    count_old_links += 1
            if count_old_links >= items_per_unit:
                return True

    return False


def applicables(elements_per_units, old_links, config, own_validator):
    """Loop the units and validate each item in a unit.

    :param elements_per_units:
    :param config:
    :param own_validator:
    """
    rules = config['rules']
    replaces_at_all = rules.get('replaces_at_all')
    items_per_unit = rules.get('items_per_unit')
    sort_by_item_value = rules.get('sort_by_item_value')

    candidates = []
    i = 0

    for from_to_string, elements in elements_per_units:
        i += 1

        u_from, u_to, u_string = from_to_string
        log("UNIT {} {}".format(i, from_to_string))

        if len(elements) is 0:
            log("continue, c: {}, raa: {}".format(len(candidates),
                                                  replaces_at_all))
            continue

        if sort_by_item_value:
            key = sort_by_item_value['key']
            default = sort_by_item_value['default']
            elements = sorted(elements,
                              key=lambda tup: tup[3].get(key, default),
                              reverse=True)
            log("elements: {}".format(
                [(e, f.get(key, default)) for _, _, e, f in elements]))
        else:
            log("elements: {}".format([e for _, _, e, _ in elements]))

        # # 1. replaces_at_all
        if replaces_at_all and len(candidates) >= replaces_at_all:
            log("break of replaces_at_all: {}".format(
                replaces_at_all))
            return the_applicables(candidates, config)

        unit_candidates = []
        for _from, _to, token, element in elements:
            # # check the rules
            # # 1. replaces_at_all
            if replaces_at_all and len(candidates) >= replaces_at_all:
                log("break of replaces_at_all: {}".format(
                    replaces_at_all))
                return the_applicables(candidates, config)

            # we need to check this already before first candidate
            if items_per_unit_satisfied(items_per_unit, unit_candidates, old_links, u_from, u_to):
                log("break of items_per_unit: {}".format(
                    items_per_unit))
                break

            candito = (token, element)
            if candidate.valid(candito, candidates, unit_candidates,
                    rules, old_links, own_validator):

                log(u"valid: {} (uc: {}, c:{})".format(
                    token, len(unit_candidates), len(candidates)))

                candidates.append((_from, _to, token, element))
                unit_candidates.append((_from, _to, token, element))

                # # 2. text_unit > number_of_items

                if items_per_unit_satisfied(items_per_unit, unit_candidates, old_links, u_from, u_to):
                    log("break of items_per_unit: {}".format(
                        items_per_unit))
                    break
            else:
                log(u"invalid candidate: {}".format(token))

    return the_applicables(candidates, config)
