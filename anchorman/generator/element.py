# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

from anchorman.generator.highlight import augment_highlight
from anchorman.generator.highlight import create_highlight
from anchorman.generator.tag import augment_bs4tag
from anchorman.generator.tag import create_bs4tag
from anchorman.logger import log


def create_element_pattern(mode, markup):
    """Create the basic element pattern based on mode and markup."""

    try:
        markup = markup[mode]

        if mode == 'tag':
            pattern = create_bs4tag(markup)

        elif mode == 'highlight':
            pattern = create_highlight(markup)

        else:
            raise NotImplementedError

    except KeyError, e:
        log("KeyError: %s" % e)
        raise KeyError

    return pattern


def create_element(element_pattern, item, mode, markup):
    """Create the element that will be inserted in the text."""

    markup = markup[mode]
    _element = item.data[1][1]
    original = item.data[0]

    if mode == 'tag':
        element = augment_bs4tag(element_pattern, _element, markup, original)
    else:
        element = augment_highlight(element_pattern, original)

    return element


def remove_elements(text, markup, mode):
    """Remove elements of text based on the markup specifications."""

    success = False

    if mode == 'tag':
        text_soup = BeautifulSoup(text, "lxml")

        # use markup info to specify the element you want to find
        attributes = markup[mode].get('attributes')
        tag = markup[mode].get('tag')
        spfndll = text_soup.findAll
        anchormans = spfndll(tag, attributes) if attributes else spfndll(tag)

        for x in anchormans:
            # use re.sub vs replace to prevent encoding issues
            str_x = str(x).replace('=""', '')
            text = re.sub(str_x, x.text, text)

        success = True
        text = text.encode('utf-8')

    elif mode == 'highlight':
        markup_mode = markup[mode]
        pre, post = markup_mode['pre'], markup_mode['post']
        text = text.replace(pre, '').replace(post, '')
        success = True

    else:
        raise NotImplementedError

    return success, text
