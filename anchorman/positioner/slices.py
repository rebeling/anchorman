# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from anchorman.positioner.slices_utils import check_forbidden_areas
from anchorman.positioner.slices_utils import token_regexes
from anchorman.positioner.slices_utils import check_links_inside_tags


def element_slices(text, elements, config):
    """Get slices of all elements in text.

    :param text:
    :param elements:
    :param config:
    """
    case_sensitive = config['rules']['case_sensitive']
    element_identifier = config['settings']['element_identifier']
    token_regex = re.compile(token_regexes(elements, case_sensitive))

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


def unit_slices(text, config):
    """Slices for all units.

    :param text:
    :param config:
    """
    # from bs4.diagnose import diagnose
    # data = open("bad.html").read()
    # diagnose(data)
    settings = config['settings']
    text_unit_key = settings['text_unit']['key']
    forbidden_areas = settings['text_unit'].get('forbidden_areas', {})

    soup = BeautifulSoup(text, settings.get('parser', 'lxml'))
    soup_string = str(soup)

    # clean up automated augmentation
    if soup_string.startswith('<html><body>'):
        soup_string = soup_string[12:-14]

    soup_find_all = soup.findAll(True)

    text_units_generator = units_gen(
        soup_find_all, soup_string, text_unit_key)

    forbidden = check_forbidden_areas(
        soup_find_all, forbidden_areas, soup_string, settings)

    return text_units_generator, forbidden, soup_string


def units_gen(soup_findAll, soup_string, text_unit_key):
    for a_tag in soup_findAll:
        the_tag_str = str(a_tag)
        if a_tag.name == text_unit_key:
            try:
                # # bs4 wrongly aumgmented string?!
                _from = soup_string.index(the_tag_str)
                yield (_from, _from + len(the_tag_str), the_tag_str)
            except ValueError as e:
                # log it
                print "substring not found: %s" % a_tag
                pass
