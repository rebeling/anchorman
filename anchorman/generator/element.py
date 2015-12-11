# -*- coding: utf-8 -*-
from anchorman.generator.highlight import augment_highlight
from anchorman.generator.highlight import create_highlight
from anchorman.generator.tag import augment_bs4tag
from anchorman.generator.tag import create_bs4tag


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

    except KeyError:
        raise KeyError

    return pattern


def create_element(element_pattern, item, mode, markup):
    """Create the element that will be inserted in the text."""

    markup = markup[mode]

    if mode == 'tag':
        element = augment_bs4tag(element_pattern, item.data[1][1], markup)
    else:
        # elif mode == 'highlight':
        element = augment_highlight(element_pattern, item.data[1][1])

    return element
