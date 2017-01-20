# -*- coding: utf-8 -*-
import re
from anchorman.utils import log


def allforms(t):
    return list({t, t.lower(), t.upper(), t.title()})


def token_regexes(elements, case_sensitive):
    """Generate a regex for all tokens."""
    tokens = [e.keys()[0].encode('utf-8') for e in elements]
    forms = [[t] if case_sensitive else allforms(t) for t in tokens]
    patterns = [r"\b{0}\b".format(f) for form in forms for f in form]
    return "|".join(patterns)


def check_forbidden_areas(
        soup_find_all, forbidden_areas, soup_string, settings):
    """ """
    filter_tags = forbidden_areas.get('tags', [])
    filter_classes = forbidden_areas.get('classes', [])

    forbiddens = []
    for a_tag in soup_find_all:

        forbidden_tag = check_tag(a_tag, filter_tags, soup_string)

        if forbidden_tag:
            token, (_from, _to), _type = forbidden_tag
            forbiddens.append((_from, _to, token.text))

        if filter_classes:
            # could this return more than one item?
            forbidden_elements = check_classes(
                a_tag, filter_classes, soup_string)
            if forbidden_elements:
                # for forbidden_element in forbidden_elements:
                #     token, (_from, _to), _type = forbidden_element
                #     forbiddens.append((_from, _to, None))
                for forbidden_element in forbidden_elements:
                    _from, _to = forbidden_element
                    forbiddens.append((_from, _to, None))

    if settings.get('no_links_inside_tags'):
        forbiddens += check_links_inside_tags(soup_string)

    return forbiddens


def check_tag(a_tag, filter_tags, soup_string):
    """ """
    if a_tag.name in filter_tags:
        try:
            the_tag_str = str(a_tag)
            _from = soup_string.index(the_tag_str)
            return (a_tag, (_from, _from + len(the_tag_str)), ('forbidden'))
        except ValueError as e:
            log("substring not found: {}, {}".format(a_tag, e))
    return None


def check_classes(a_tag, filter_classes, soup_string):
    """ """
    try:
        _from = soup_string.index(str(a_tag))
        tag_classes = dict(a_tag.attrs).get('class', '')
        return [(_from, _from + len(str(a_tag)))
                for fclass in filter_classes
                for tclass in tag_classes
                if fclass in tclass]
    except ValueError as e:
        log("substring not found: {}, {}".format(a_tag, e))
    return None


def check_links_inside_tags(soup_string):
    """Find tag elements and mark the intervall."""
    return [(match.start(), match.end(), None)
            for match in re.finditer(r"<(\w|/).*?>", soup_string)]
