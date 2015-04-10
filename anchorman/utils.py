#!/usr/bin/env python
# -*- coding: utf-8 -*-

def sort_longest_match_first(links):
    links.sort(key=lambda c: len(c.keys()[0]), reverse=True)
    return links


def validate_input(args, _isinstance=isinstance):
    try:
        text, links = args[0], args[1]
        # evaluate format
        if not _isinstance(text, str) and not _isinstance(text, unicode):
            return False, "text (first argument) should be str/unicode"
        if not _isinstance(links, list):
            return False, "links (second argument) should be list"
    except BaseException:
        try:
            text = args[0]
        except BaseException:
            return False, "arguments text and links missing"
        try:
            links = args[1]
        except BaseException:
            return False, "second argument is missing"
    return True, (text, links)
