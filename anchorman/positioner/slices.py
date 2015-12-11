# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup


def element_slices(text, elements, element_identifier):
    """Get slices of all elements in text. """

    tokens = [e.keys()[0] for e in elements]
    tokens = "|".join([r"\b{}\b".format(t) for t in tokens])
    token_regex = re.compile(tokens)

    result = []
    for match in token_regex.finditer(text):
        token, _from, _to = match.group(), match.start(), match.end()
        base = [e for e in elements if e.keys()[0] == token][0]
        result.append((token, (_from, _to), (element_identifier, base)))

    return result


def unit_slices(text, text_unit):
    """Get slices of the text units specified in setting."""

    text_unit_key, text_unit_name = text_unit['key'], text_unit['name']
    text_unit_pair = (text_unit_key, text_unit_name)

    result = []
    if text_unit_pair == ('t', 'text'):
        # there is only one unit the whole text
        i, _from, _to = 0, 0, len(text)
        result.append((text_unit_key, (_from, _to), (text_unit_name, i)))

    elif text_unit_name.startswith(('html', 'xml')):
        soup = BeautifulSoup(text, "lxml")
        for i, a_text_unit in enumerate(soup.find_all(text_unit_key)):
            a_text_unit = str(a_text_unit)
            _from = text.index(a_text_unit)
            _to = _from + len(a_text_unit)
            result.append((text_unit_key, (_from, _to), (text_unit_name, i)))

    # todo
    # elif text_unit_pair == ('s', 'sentence'):
    #     # use some external library or at least have it in mind

    else:
        raise NotImplementedError

    return result
