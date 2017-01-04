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
                               (element_identifier, base)))

    return element_slices


def unit_slices(text, config):
    """Get slices of the text units specified in settings.

    :param text:
    :param config:
    """
    text_unit_key = config['settings']['text_unit']['key']
    text_unit_name = config['settings']['text_unit']['name']

    units, forbidden = [], []

    if (text_unit_key, text_unit_name) == ('t', 'text'):
        # the whole text is one unit
        units.append((text_unit_key, (0, len(text)), (text_unit_name, 0)))
    elif text_unit_name.startswith(('html', 'xml')):
        # the text need to be parsed to get its structure
        units, forbidden = parse_units(text, config['settings'])
    else:
        raise NotImplementedError

    return units, forbidden


def parse_units(text, settings):
    """

    :param text:
    :param settings:
    """
    # from bs4.diagnose import diagnose
    # data = open("bad.html").read()
    # diagnose(data)

    text_unit_key = settings['text_unit']['key']
    forbidden_areas = settings['text_unit'].get('forbidden_areas', {})
    soup = BeautifulSoup(text, settings.get('parser', 'lxml'))
    all_tags = soup.findAll(True)
    soup_string = str(soup)
    text_units, forbidden = [], []

    if soup_string.startswith('<html><body>'):
        soup_string = soup_string[12:-14]
        # print "soup_string", soup_string

    for i, a_tag in enumerate(all_tags):
        the_tag_str = str(a_tag)
        if a_tag.name == text_unit_key:
            try:
                # # bs4 wrongly aumgmented string?!
                _from = soup_string.index(the_tag_str)
                text_units.append((a_tag,
                                   (_from, _from + len(the_tag_str)),
                                   (text_unit_key, i)))
            except ValueError as e:
                # log it
                print "substring not found: %s" % a_tag
                pass

        if forbidden_areas:
            forbidden += check_forbidden_areas(a_tag,
                                               forbidden_areas,
                                               soup_string,
                                               i)

    if settings.get('no_links_inside_tags', None):
        forbidden += check_links_inside_tags(soup_string)

    return text_units, forbidden
