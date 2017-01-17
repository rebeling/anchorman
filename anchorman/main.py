# -*- coding: utf-8 -*-
from anchorman.configuration import get_config
from anchorman.validator.find_hits import applicables
from anchorman.generator import augment_result, remove_elements
from anchorman.positioner.interval import intervals
from anchorman.utils import filter_applied_against_input
# from anchorman.utils import timeit

# @timeit
def annotate(text, elements, own_validator=None, config=get_config(
        include_project_config=False)):
    """Find and annotate elements in text.

    Create an invaltree with elements and units of text, validate
    the rules to apply elements and augment the text with this result.
    """
    units, etree = intervals(text, elements, config)
    to_be_applied = applicables(units, etree, config, own_validator)

    # apply the items, but start at the end ...its not like horse riding!
    text = augment_result(text, to_be_applied)

    if config['settings'].get('return_applied_links'):
        applied, rest = filter_applied_against_input(elements, to_be_applied)
        return text, applied, rest

    return text


def clean(text, config=get_config(include_project_config=False)):
    """Remove elements from text based on mode and markup.

    Use config data to identify markup elements in the text and remove them.
    :param config:
    :param text:
    """
    return remove_elements(text, config)
