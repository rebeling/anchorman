# -*- coding: utf-8 -*-
import logging
from anchorman.configuration import get_config
from anchorman.validator.find_hits import applicables
from anchorman.generator import augment_result, remove_elements
from anchorman.positioner.interval import intervals
from anchorman.utils import filter_applied_against_input
# from anchorman.utils import timeit
from anchorman.utils import log
from anchorman.utils import set_and_log_level


# @timeit
def annotate(text, elements, own_validator=None,
             config=get_config(include_project_config=False)):
    """Find and annotate elements in text.

    Create an invaltree with elements and units of text, validate
    the rules to apply elements and augment the text with this result.
    """
    set_and_log_level(config['settings']['log_level'])
    log('starting debugging')

    units, old_links, soup_string = intervals(text, elements, config)
    to_be_applied = applicables(units, old_links, config, own_validator)

    log(soup_string)
    log(soup_string[949:953])

    log('{} of {} to_be_applied'.format(len(to_be_applied), len(elements)))

    # apply the items, but start at the end ...its not like horse riding!
    text = augment_result(soup_string, to_be_applied)

    log(text)

    if config['settings'].get('return_applied_links'):
        applied, rest = filter_applied_against_input(elements, to_be_applied)
        log('end of debugging\n')
        return text, applied, rest

    log('end of debugging\n')
    return text


def clean(text, config=get_config(include_project_config=False)):
    """Remove elements from text based on mode and markup.

    Use config data to identify markup elements in the text and remove them.
    :param config:
    :param text:
    """
    return remove_elements(text, config)
