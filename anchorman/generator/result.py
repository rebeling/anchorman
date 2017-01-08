# -*- coding: utf-8 -*-


def augment(text, to_be_applied):
    """Augment the text with the elements in to be applied.

    :param text:
    :param to_be_applied:
    """
    _pattern = "{}{}{}"
    to_be_applied = sorted(to_be_applied, reverse=True)

    for interval, element in to_be_applied:
        text = _pattern.format(text[:interval.begin],
                               element,
                               text[interval.end:])
    return text


def filter_applied_against_input(elements, to_be_applied):
    """Return a tuple of applied items and the rest."""
    applied = [item[0].data[1][1] for item in to_be_applied]
    rest = [x for x in elements if x not in applied]
    return applied, rest
