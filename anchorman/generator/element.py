# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
from anchorman.generator.highlight import augment_highlight
from anchorman.generator.highlight import create_highlight
from anchorman.generator.tag import augment_bs4tag
from anchorman.generator.tag import create_bs4tag
from anchorman.logger import log


def create_element_pattern(mode, markup, parser):
    """Create the basic element pattern based on mode and markup.

    :param markup:
    :param mode:
    """
    try:
        if mode == 'tag':
            pattern = create_bs4tag(markup[mode], parser)
        elif mode == 'highlight':
            pattern = create_highlight(markup[mode])
        else:
            raise NotImplementedError
    except KeyError, e:
        log("KeyError: %s" % e)
        raise KeyError

    return pattern


def create_element(item, config):
    """Create the element that will be inserted in the text.

    :param markup:
    :param mode:
    :param item:
    :param element_pattern:
    """
    markup = config['markup']
    settings = config['settings']
    mode = settings['mode']

    element_pattern = create_element_pattern(mode,
                                             markup,
                                             settings.get('parser', 'lxml'))
    _element = item.data[1][1]
    original = item.data[0]

    if mode == 'tag':
        element = augment_bs4tag(
            element_pattern, _element, markup[mode], original)
    else:
        element = augment_highlight(element_pattern, original)

    return element


def remove_elements(text, config):
    """Remove elements of text based on the markup specifications.

    :param config:
    :param text:
    """
    mode = config['settings']['mode']
    markup_mode = config['markup'][mode]

    success = False
    if mode == 'tag':
        text_soup = BeautifulSoup(text,
                                  config['settings'].get('parser', 'lxml'))

        # use markup info to specify the element you want to find
        found = text_soup.findAll
        attributes = markup_mode.get('attributes')
        tag = markup_mode.get('tag')
        anchors = found(tag, attributes) if attributes else found(tag)

        for anchor in anchors:
            id_string = specified_or_guess(markup_mode, attributes)
            anchor_text = anchor.text.encode('utf-8')
            fuzzy = fuzzy_regex(tag, id_string, anchor_text)
            # use re.sub vs replace to prevent encoding issues
            text = re.sub(fuzzy, anchor_text, text)
        success = True

    elif mode == 'highlight':
        pre, post = markup_mode['pre'], markup_mode['post']
        text = text.replace(pre, '').replace(post, '')
        success = True

    else:
        raise NotImplementedError

    return success, text


def specified_or_guess(markup_mode, attributes):
    """"""
    identifier = markup_mode.get('identifier')
    key, value = identifier.items()[0] if identifier else attributes.items()[0]
    return '{}="{}"'.format(key, value)


def fuzzy_regex(tag, id_string, anchor_text):
    """"""
    return "<{0}.*?{1}[^>]*?>{2}<\/{0}>".format(tag, id_string, anchor_text)
