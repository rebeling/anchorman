# -*- coding: utf-8 -*-


def augment(text, to_be_applied):
    """Augment the text with the elements in to be applied."""

    x = "{}{}{}"
    for interval, element in reversed(to_be_applied):
        text = x.format(text[:interval.begin],
                        element,
                        text[interval.end:])
    return text
