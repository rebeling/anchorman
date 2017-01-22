# -*- coding: utf-8 -*-
# from anchorman.utils import log
import re

from bs4 import BeautifulSoup
from anchorman.utils import check_tags, check_classes, log


def unit_slices(text, the_soup, settings):
    """Slices for all units.

    # from bs4.diagnose import diagnose
    # data = open("bad.html").read()
    # diagnose(data)

    :param text:
    :param config:
    """
    return (units_gen(the_soup, settings), proof_areas(the_soup, settings))


def units_gen(the_soup, settings):

    text_unit_key = settings['text_unit']['key']
    soup, soup_str = the_soup
    for a_tag in soup.findAll(True):
        if a_tag.name == text_unit_key:
            try:
                the_tag_str = str(a_tag)
                # # bs4 wrongly aumgmented string?!
                _from = soup_str.index(the_tag_str)
                yield (_from, _from + len(the_tag_str), the_tag_str)
            except ValueError as e:
                log("substring not found: {}, {}".format(the_tag_str, e))


def proof_areas(the_soup, settings):
    """ """
    forbidden_areas = settings.get('forbidden_areas', {})

    soup, soup_str = the_soup
    tags = forbidden_areas.get('tags', [])
    classes = forbidden_areas.get('classes', [])

    forbiddens = []
    for a_tag in soup.findAll(True):
        # find forbidden tags
        forbidden_tag = check_tags(a_tag, tags, soup_str)
        if forbidden_tag:
            forbiddens.append(forbidden_tag)
        # find forbidden elements by class
        for forbidden_element in check_classes(a_tag, classes, soup_str):
            forbiddens.append(forbidden_element)

    if settings.get('no_links_inside_tags'):
        # find tag elements and mark the intervall
        forbiddens += [(match.start(), match.end(), None)
                       for match in re.finditer(r"<(\w|/).*?>", soup_str)]

    return forbiddens
