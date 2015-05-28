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


def linker_format(link_format):
    new_link_format, selector = None, None
    if link_format:
        rmtuple = None
        if 'rm-identifier' in link_format:
            rmtuple = ("data-rm-key", link_format['rm-identifier'])
            rm = link_format.get('attributes', [])
            rm.append(rmtuple)
            link_format['attributes'] = rm
        tag = link_format.get('tag', None)
        if tag:
            if rmtuple:
                selector = './/%s[@%s="%s"]' % (tag, rmtuple[0], rmtuple[1])
        # else do not overwrite the default self.selector
        new_link_format = {
            'tag': link_format.get('tag', 'a'),
            'value_key': link_format.get('value_key', 'href'),
            'attributes': link_format.get('attributes', [])
            }
    return new_link_format, selector


def re_pattern_of(key, case_sensitive=True):

    if type(key) is str:
        key = [key]

    re_words = []
    for k in key:
        w = k.replace('.', '\.')
        if case_sensitive:
            re_words.append(w)
        else:
            re_words += list(set([w, w.title(), w.lower(), w.upper()]))

    re_words = '|'.join(re_words)
    re_capture = u"(^|[^\w\-/äöüßÄÖÜ])(%s)([^\w\-/äöüßÄÖÜ]|$)" % re_words

    return re_words, re_capture
