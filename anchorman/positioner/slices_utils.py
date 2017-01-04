# -*- coding: utf-8 -*-
import re


def allforms(t):
    return list({t, t.lower(), t.upper(), t.title()})


def token_regexes(elements, case_sensitive):
    """Generate a regex for all tokens."""
    tokens = [e.keys()[0].encode('utf-8') for e in elements]
    forms = [[t] if case_sensitive else allforms(t) for t in tokens]
    patterns = [r"\b{0}\b".format(f) for form in forms for f in form]
    return "|".join(patterns)


def check_forbidden_areas(a_tag, forbidden_areas, soup_string, i):
    """ """
    filter_tags = forbidden_areas.get('tags', [])
    filter_classes = forbidden_areas.get('classes', [])

    forbiddens = []
    forbidden_tag = check_tag(a_tag, filter_tags, soup_string, i)
    if forbidden_tag:
        forbiddens.append(forbidden_tag)
    if filter_classes:
        # could this return more than one item?
        forbidden_elements = check_classes(
            a_tag, filter_classes, soup_string, i)
        if forbidden_elements:
            for forbidden_element in forbidden_elements:
                forbiddens.append(forbidden_element)
    return forbiddens


def check_tag(a_tag, filter_tags, soup_string, i):
    """ """
    if a_tag.name in filter_tags:
        try:
            the_tag_str = str(a_tag)
            _from = soup_string.index(the_tag_str)
            return (a_tag, (_from, _from + len(the_tag_str)), ('forbidden', i))
        except ValueError as e:
            # log it
            print "substring not found: %s" % a_tag
            pass
    return None


def check_classes(a_tag, filter_classes, soup_string, i):
    """ """
    elements = []
    tag_classes = dict(a_tag.attrs).get('class', '')
    for fclass in filter_classes:
        for tclass in tag_classes:
            if fclass in tclass:
                try:
                    the_tag_str = str(a_tag)
                    _from = soup_string.index(the_tag_str)
                    elements.append(
                        (a_tag,
                         (_from, _from + len(the_tag_str)),
                         ('forbidden', i)))
                except ValueError as e:
                    # log it
                    print "substring not found: %s" % a_tag
                    pass
    return elements


def check_links_inside_tags(soup_string):
    """ """
    forbiddens = []
    tag_regex = re.compile(r"<(\w|/).*?>", re.DOTALL)
    for match in tag_regex.finditer(soup_string):
        forbiddens.append((match.group(),
                           (match.start(), match.end()),
                           ('insidetag', None)))
    return forbiddens
