# -*- coding: utf-8 -*-


def augment(text, to_be_applied):
    """Augment the text with the elements in to be applied.
    :param text:
    :param to_be_applied:
    """

    _pattern = "{}{}{}"
    for interval, element in reversed(to_be_applied):
        text = _pattern.format(text[:interval.begin],
                               element,
                               text[interval.end:])
    return text
