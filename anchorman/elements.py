# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from anchorman.utils import tokens_as_re, log, soup_it


def element_slices(text, elements, rules):
    """Get slices of all elements in text.

    :param text:
    :param elements:
    :param config:
    """
    case_sensitive = rules['case_sensitive']
    token_regex = re.compile(tokens_as_re(elements, case_sensitive))

    element_slices = []
    element_slices_append = element_slices.append

    for match in token_regex.finditer(text):
        token = match.group()
        base = None

        for element in elements:
            check_element = element.keys()[0].encode('utf-8')
            check_token = token

            if case_sensitive is False:
                check_element = check_element.lower()
                check_token = check_token.lower()

            if check_element == check_token:
                base = element
                break

        element_slices_append(match.span()+(token, base.values()[0]))

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


def create_element(candidate, config):
    """Create the element that will be inserted in the text.

    :param item:
    :param config:
    """
    exclude_keys = config['markup'].get('exclude_keys', [])
    attr = config['markup'].get('attributes', {}).items()

    _from, _to, token, element = candidate
    attr += element.items()
    attributes = None
    try:
        attributes = ['{}="{}"'.format(key, val)
                      for key, val in sorted(attr)
                      if key not in exclude_keys]
    except Exception as e:
        log("{}: {}".format(attr, e))

    anchor = '<{tag}{attributes}>{text}</{tag}>'.format(
        tag=config['markup']['tag'],
        attributes=' '+' '.join(attributes) if attributes else '',
        text=token)

    return _from, _to, token, anchor


def remove_elements(text, config):
    """Remove elements of text based on the markup specifications.

    :param config:
    :param text:
    """
    # soup_it
    soup, _ = soup_it(text, config['settings'])
    attributes = config['markup'].get('attributes')
    tag = config['markup'].get('tag')

    found = soup.findAll
    anchors = found(tag, attributes) if attributes else found(tag)

    for anchor in anchors:
        anchor_text = anchor.text.encode('utf-8')
        fuzzy_re = "<{0}[^>]*?{1}[^>]*?>{2}<\/{0}>".format(
            tag, specified_or_guess(config['markup'], attributes),
            anchor_text)
        # use re.sub vs replace to prevent encoding issues
        text = re.sub(fuzzy_re, anchor_text, text)

    return text


def specified_or_guess(markup, attributes):
    """"""
    identifier = markup.get('identifier')
    key, value = identifier.items()[0] if identifier else attributes.items()[0]
    return '{}="{}"'.format(key, value)
