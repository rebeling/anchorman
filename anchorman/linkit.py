#!/usr/bin/env python
# encoding: utf-8

import re
from lxml import etree

from tree import to_tree, from_tree


class Anchorman(object):
    """ 
    Create the main object for the add_links request.
    """
    def __init__(self, html, links, text, counts, **kwargs):
        self.original = html
        self.links = links
        self.text = text
        self.counts = counts

    def __str__(self):
        return self.text


def remove_links(content, selector='.//a[@class="anchorman"]'):
    """
    Takes a string of HTML or text and removes all the tags 
    - specified by selector - and leaves their content.
    """
    try:
        root = to_tree(content)
        to_remove = root.xpath(selector)
        for element in to_remove:
            element.tag = "to-remove"
            etree.strip_tags(root, "to-remove")
        return from_tree(root)
    except Exception, e:
        return 'exception: %s' % e


def link_fn(key, value, match):
    """ 
    The link object
    todo: make it available for personalization of Element and attrib
    """
    element = etree.Element('a')
    element.attrib["class"] = "anchorman"
    element.attrib["href"] = value
    element.text = match
    return element


def ignore_fn(element):
    """
    Do not replace and element in itself.
    todo: use a customized class selector, default anchorman
    """
    if "anchorman" in element.get("class", ""):
        return True
    return False


def replace_in_element(element, key, value, replacement_fn, replaces=None,
        ignore_fn=lambda x: False):

    re_word = key.replace('.', '\.')
    re_capture = u"([^\wäöüßÄÖÜ])(%s)([^\wäöüßÄÖÜ])" % re_word
    count = 0

    if element.tail is not None and not ignore_fn(element.getparent()):
        match = re.search(re_capture, " %s " % element.tail)
        if match:
            count += 1
            text = element.tail
            new_link = replacement_fn(key, value, match.groups(1)[1])
            element.addnext(new_link)

            if match.start() == 0:
                element.tail = ""
            else:
                element.tail = text[:match.start() - 1] + match.groups()[0]

            if match.start() + len(''.join(match.groups())) == len(text) + 2:
                new_link.tail = ""
            else:
                new_link.tail = match.groups()[2] + text[match.start()+len(match.groups()[1])+1:]

            if replaces and replaces == count:
                return count

    if element.text is not None and not ignore_fn(element):
        match = re.search(re_capture, " %s " % element.text)
        if match:
            count += 1
            text = element.text
            new_link = replacement_fn(key, value, match.groups(1)[1])

            if match.start() == 0:
                element.text = ""
            else:
                element.text = text[:match.start()-1] + match.groups()[0]

            if match.start() + len(''.join(match.groups())) == len(text) + 2:
                new_link.tail = ""
            else:
                new_link.tail = match.groups()[2] + text[match.start()+len(match.groups()[1])+1:]

            element.insert(0, new_link)

            if replaces and count == replaces:
                return count

    return count 


def replace_token(content, key, value, replacement_fn, count=0, replaces=None):
    """
    Takes content as a string, a match to replace and the repacement.

    Updates content with all matches of the "key" variable and surrounds them
    with an "a" tag with a class "in-text-link" and a href of the "value"
    variable. The key string is not case sensitive and it will only surround
    matches of the key string that are not surround by other letters, it tries
    to match whole words.

    Ruturns a tuple with the updated content and the number of replacements
    made.

    """
    root = to_tree(content)

    for element in root.iter():
        count = replace_in_element(element, key, value, replacement_fn, 
            replaces=replaces, ignore_fn=ignore_fn)

        if replaces and count == replaces:
            return (from_tree(root), count)

    return (from_tree(root), count)


def add_links(html, links, **kwargs):
    """
    Takes html and a dictionary of words to highlight and links. Surrounds
    the matched words with a specified html element - by default a link.
    """
    replacement_format = link_fn
    enriched = reduce(lambda acc, val: 
        replace_token(acc, 
                      val[0], 
                      val[1], 
                      replacement_format, 
                      replaces=kwargs.get('replaces', None))[0],
        dict(links).iteritems(),
        html
    )
    # todo: add the counts for eaach item ...may position too
    counts = [1]
    return Anchorman(html, links, enriched, counts, **kwargs)


if __name__ == "__main__":
    text = '<p>The quick brown fox. jumps over the lazy dog.</p>'
    links = [('fox', 'http://en.wikipedia.org/wiki/Fox'), ('mammals', 'http://en.wikipedia.org/wiki/Mammal')]
    # counts should be = [1, 0]
    # print replace_token(text, "Fox.", "hello", link_fn)
    a = add_links(text, links)
    print a
    print remove_links(a.text)
