# -*- coding: utf-8 -*-
from anchorman.configure import get_config
from anchorman.generator.candidate import retrieve_hits
from anchorman.generator.text import augment
from anchorman.positioner.interval import intervals

# from utils import pretty


def annotate(text, elements, config=get_config(project_conf=False)):
    """Find and annotate elements in text.

    Create an invaltree with elements and units of text, validate the rules
    to apply elements and augment the text with this result.

    Args:
        text (str): The first parameter.
        elements (list): The second parameter. Defaults to None.
            Second line of description should be indented.
        config (dict): Load default config from etc/

    Returns:
        bool: True if successful, False otherwise.

        The return type is optional and may be specified at the beginning of
        the ``Returns`` section followed by a colon.

        The ``Returns`` section supports any reStructuredText formatting,
        including literal blocks::

            {
                'param1': param1,
                'param2': param2
            }

    Examples:
        Examples should be written in doctest format, and should illustrate how
        to use the function.

        >>> print([i for i in example_generator(4)])
        [0, 1, 2, 3]

    """
    intervaltree, units = intervals(text, elements, config['setting'])
    to_be_applied = retrieve_hits(intervaltree, units, config)

    # apply the items finally, but start from end ...its not like horse riding!
    text = augment(text, to_be_applied)
    return text

# text = '<p class="first">The qüick brown fox jumps</p> <p>over the lazy dog in Los Angeles.</p>'

# elements = [
#     {'qüick': {
#         'value': '/wiki/queick',
#         'score': 0.2,
#         'type': 'jj'}},
#     {'fox': {
#         'value': '/wiki/fox',
#         'score': 23.0,
#         'type': 'animal'}},
#     {'lazy': {
#         'value': '/wiki/lazy',
#         'score': 5.55,
#         'type': 'jj'}},
#     {'dog': {
#         'value': '/wiki/dog',
#         'score': 12.0,
#         'type': 'animal'}},
#     {'Los Angeles': {
#         'value': '/wiki/los-angeles',
#         'score': 42.0,
#         'type': 'city'}}
#     ]

# annotated = annotate(text, elements)
# print annotated

# # cfg = get_config()
# # print cfg
# # cfg['setting']['mode'] = 'highlight'
# # annotated = annotate(text, elements, config=cfg)
# # print annotated
