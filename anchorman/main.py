# -*- coding: utf-8 -*-
from anchorman.configuration import get_config
from anchorman.generator.candidate import retrieve_hits
from anchorman.generator.text import augment
from anchorman.positioner.interval import intervals


def annotate(text,
             elements,
             own_validator=[],
             config=get_config(project_conf=False)):
    """Find and annotate elements in text.

    Create an invaltree with elements and units of text, validate the rules
    to apply elements and augment the text with this result.

    Args:
        text (str): The first parameter.
        elements (list): It is a list of element dicts like the following:
            {'fox': {'value': '/wiki/fox', 'data-type': 'animal'}}
        own_validator (list): A list of functions that will be applied in the
            validation of an element, if it will be applied in the text.
        config (dict): Load default config from etc/ or get_config the default
            config andd update to your own rules.

    Returns:
        text (str): The annotated text.

    Examples:
        Basic example with overwriting the config:

        >>> text = 'The qüick brown fox jumps over the lazy dog in Los Angeles.'
        >>> elements = [{'fox': {'value': '/wiki/fox', 'data-type': 'animal'}},
                        {'dog': {'value': '/wiki/dog', 'data-type': 'animal'}}]
        >>> cfg = get_config()
        >>> cfg['setting']['replaces_at_all'] = 1
        >>> print annotate(text, elements, config=cfg)
        'The qüick brown <a href="/wiki/fox" data-type="animal">fox</a> jumps over the lazy dog in Los Angeles.'

    """
    intervaltree, units = intervals(text, elements, config['setting'])
    to_be_applied = retrieve_hits(intervaltree, units, config, own_validator)

    # apply the items finally, but start from end ...its not like horse riding!
    text = augment(text, to_be_applied)
    return text
