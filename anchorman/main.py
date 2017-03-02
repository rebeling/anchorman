# -*- coding: utf-8 -*-
from anchorman.elements import create_element
from anchorman.elements import remove_elements
from anchorman.intervals import all_intervals
from anchorman.result import applicables
from anchorman.result import augment_result
from anchorman.settings import get_config
from anchorman.utils import log
from anchorman.utils import set_and_log_level

# from anchorman.utils import timeit, do_profile

# import objgraph
# # print objgraph.show_most_common_types()
# roots = objgraph.get_leaking_objects()
# objgraph.show_most_common_types(objects=roots)
# objgraph.show_refs(roots[:3], refcounts=True, filename='roots.png')


# @timeit
# @do_profile()
def annotate(text, elements, own_validator=None,
             config=get_config(include_project_config=False)):
    """Find and annotate elements in text.

    Create an invaltree with elements and units of text, validate
    the rules to apply elements and augment the text with this result.
    """
    set_and_log_level(config['settings']['log_level'])
    # log('starting debugging')

    units, old_links, soup_string = all_intervals(text, elements, config)
    to_be_applied = applicables(units, old_links, config, own_validator)

    markup = config['markup']
    decorate_markup = markup.get('decorate')
    return_applied_links = config['settings'].get('return_applied_links')

    if return_applied_links:
        rest = [{e[2]: e[3]} 
                for _, ele in units 
                for e in ele 
                if e not in to_be_applied]

    rest_anchors = []
    if decorate_markup:
        rest_anchors = [create_element(e, markup)
                        for _, ele in units 
                        for e in ele 
                        if e not in to_be_applied]

    anchors = [create_element(c, markup, anchor=True) for c in to_be_applied]

    # log(soup_string)
    # log(soup_string[949:953])
    # log('{} of {} to_be_applied'.format(len(to_be_applied), len(elements)))

    # apply the items, but start at the end ...its not like horse riding!
    text = augment_result(soup_string, anchors + rest_anchors)

    # log(text)

    if return_applied_links:
        applied = [e for a, _, _, _, e in anchors]
        return text, applied, rest

    # log('end of debugging\n')
    return text


def clean(text, config=get_config(include_project_config=False)):
    """Remove elements from text based on mode and markup.

    Use config data to identify markup elements in the text and remove them.
    :param config:
    :param text:
    """
    return remove_elements(text, config)
