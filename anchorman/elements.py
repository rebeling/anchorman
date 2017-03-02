# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from anchorman.utils import tokens_as_re
from anchorman.utils import log
from anchorman.utils import soup_it


def element_slices(text, elements, rules):
    """Get slices of all elements in text.

    :param text:
    :param elements:
    :param config:
    """
    case_sensitive = rules['case_sensitive']
    tar = tokens_as_re(elements, case_sensitive)
    log(tar)
    token_regex = re.compile(tar)

    element_slices = []
    element_slices_append = element_slices.append

    for match in token_regex.finditer(text):
        token = match.group()
        base = None

        for element in elements:
            check_element = list(element)[0]
            check_token = token

            if case_sensitive is False:
                check_element = check_element.lower()
                check_token = check_token.lower()

            if check_element == check_token:
                base = element
                break

        element_slices_append(match.span()+(token, list(base.values())[0]))

    return element_slices


def elements_per_unit(units, forbidden, data):
    """Create an interval generator for elemets in units.

    :param forbidden:
    :param data:
    """
    lookup = {x for f, t, token in forbidden for x in range(f, t)}
    for _from, _to, string in units:
        yield ((_from, _to, string),
               [(t_from, t_to, token, element)
                for t_from, t_to, token, element in data
                if t_from not in lookup and t_to - 1 not in lookup
                # check if element fits the unit
                if _from < t_from and t_to < _to])


def create_element(candidate, markup, anchor=False):
    """Create the element that will be inserted in the text.

    :param candidate: a candidate from links input
    :param config: anchorman configuration, setup.yml
    """
    _from, _to, token, element = candidate
    anchor_str = format_element(candidate, markup, anchor)

    return (_from, _to, token, anchor_str, {token: element})


def format_element(candidate, markup, anchor):
    """Format the anchor the why you want overwrite me!

    Beware of markup rest!
    Markup rest is called when specified, on the rest of the elements.
    """
    _from, _to, token, element = candidate
    if 'token' not in element:
        element['token'] = token

    if anchor:
        anchor_pattern = markup.get('anchor_pattern')
        the_anchor = anchor_pattern.format(**element)
    else:
        the_anchor = token

    element.update({markup.get('decorate_anchor_key'): the_anchor})

    decorate_markup = markup.get('decorate')

    if decorate_markup:
        decorate_pattern = decorate_markup.get('decorate_pattern')
        decorated = decorate_pattern.format(**element)
    else:
        decorated = the_anchor

    anchorman = decorated
    return anchorman


def remove_elements(text, config):
    """Remove elements of text based on the markup specifications.

    :param config: anchorman configuration, setup.yml
    :param text: input text
    """
    # soup_it
    soup, _ = soup_it(text, config['settings'])
    attributes = config['markup'].get('rm_identifier')
    rm_tag = config['markup'].get('rm_tag')

    found = soup.findAll
    anchors = found(rm_tag, attributes) if attributes else found(rm_tag)

    for anchor in anchors:
        anchor_text = anchor.text
        fuzzy_re = "<{0}[^>]*?{1}[^>]*?>{2}<\/{0}>".format(
            rm_tag, specified_or_guess(config['markup'], attributes),
            anchor_text)
        # use re.sub vs replace to prevent encoding issues
        text = re.sub(fuzzy_re, anchor_text, text)

    return text


def specified_or_guess(markup, attributes):
    """Without identifier guess the elements to be removed based on markup.

    :param config: anchorman markup from setup.yml
    :param text: element attributes or identifier
    """
    identifier = markup.get('rm_identifier')
    first_attribute = list(attributes.items())[0]
    key, value = list(identifier.items())[0] if identifier else first_attribute
    return '{}="{}"'.format(key, value)
