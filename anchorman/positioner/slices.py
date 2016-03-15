# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup


def allforms(t):
    return list(set([t, t.lower(), t.upper(), t.title()]))


def token_regexes(elements, case_sensitive):

    tokens = [e.keys()[0].encode('utf-8') for e in elements]
    forms = [[t] if case_sensitive else allforms(t) for t in tokens]
    patterns = [r"\b{0}\b".format(f) for form in forms for f in form]

    return "|".join(patterns)


def element_slices(text, elements, settings):
    """Get slices of all elements in text. """

    case_sensitive = settings['case_sensitive']
    token_regex = re.compile(token_regexes(elements, case_sensitive))

    element_slices = []
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

        element_slices.append((token,
                               (match.start(), match.end()),
                               (settings['element_identifier'], base)))
    return element_slices


def unit_slices(text, text_unit_key, text_unit_name):
    """Get slices of the text units specified in settings."""

    units = []
    if (text_unit_key, text_unit_name) == ('t', 'text'):
        # the whole text is one unit
        units.append((text_unit_key, (0, len(text)),
                      (text_unit_name, 0)))

    elif text_unit_name.startswith(('html', 'xml')):
        unit_soup = BeautifulSoup(text, "lxml").find_all(text_unit_key)
        for i, a_text_unit in enumerate(unit_soup):
            a_text_unit = str(a_text_unit)
            _from = text.index(a_text_unit)
            _to = _from + len(a_text_unit)
            unit = (text_unit_key, (_from, _to), (text_unit_name, i))
            units.append(unit)

    else:
        raise NotImplementedError

    return units
