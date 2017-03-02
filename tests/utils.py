# -*- coding: utf-8 -*-
from __future__ import print_function
import re


def fix_bs4_parsing_spaces(text):
    text = re.sub(u"\n <", u"\n<", text)
    text = text.replace(u'\xc2\xa0', u' ')
    text = text.replace(u'\xc2', u' ')
    text = text.replace(u'\n', u' ')
    text = re.sub(u" +", u" ", text)
    return text


def compare_results(annotated, expected):

    for i, x in enumerate(expected):
        if x != annotated[i]:
            print(">> %s" % [x, annotated[i:10]])
            break

    print("expected %s" % expected[i-30:i+150])
    print("annotated %s" % annotated[i-30:i+150])
