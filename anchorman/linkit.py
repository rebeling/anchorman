#!/usr/bin/env python
# encoding: utf-8

import re
from lxml import etree
from tree import to_tree, from_tree


def remove_links(content, selector='.//a[@class="anchorman"]', markup_format={}):
    """
    Takes a string of HTML or text and removes all the tags
    - specified by selector - and leaves their content.
    """
    if 'highlighting' in markup_format:
        # remove pre and post tags
        pre = markup_format['highlighting'].get('pre', None)
        post = markup_format['highlighting'].get('post', None)
        if pre and post:
            content = content.replace(pre, '')
            content = content.replace(post, '')
        return content
    else:
        # remove by selector
        root = to_tree(content)
        to_remove = root.xpath(selector)
        for element in to_remove:
            element.tag = "to-remove"
            etree.strip_tags(root, "to-remove")
        return from_tree(root)


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
            selector = './/%s' % (tag)
            if rmtuple:
                selector += '[@%s="%s"]' % (rmtuple[0], rmtuple[1])
        # else do not overwrite the default self.selector
        new_link_format = {
            'tag': link_format.get('tag', 'a'),
            'value_key': link_format.get('value_key', 'href'),
            'attributes': link_format.get('attributes', [])
            }
    return new_link_format, selector


def link_fn(key, value, key_attributes, match, attributes={}):
    # print 'link_fn', key, value, key_attributes, match
    # apply special attributes for every item to global attributes or iteself
    ka_applied, ka = [], {}
    if key_attributes:
        ka = dict(key_attributes)

    element = etree.Element(attributes.get('tag', 'a'))
    element.attrib[attributes.get('value_key', 'href')] = value

    for (k,v) in attributes.get('attributes', [("class", "anchorman")]):
        if k in ka:
            v = "%s %s" % (v, ka[k])
            ka_applied.append(k)
        element.attrib[k] = v

    rest = list(set(ka.keys()) - set(ka_applied))
    if rest:
        for r in rest:
            element.attrib[r] = ka[r]


    element.text = match.groups()[1]
    return element


# def ignore_fn(element):
#     """
#     Do not replace and element in itself.
#     todo: use a customized class selector, default anchorman
#     """
#     if "anchorman" in element.get("class", ""):
#         return True
#     return False


def get_newlink(key, value, key_attributes, replacement_fn, match, attributes):
    # create a new_link of the item and replace occurences
    return replacement_fn(key,
                          value,
                          key_attributes,
                          match,
                          attributes=attributes)


def replace_in_element(count, element, key, value, key_attributes, replacement_fn,
    replaces=None, attributes=None, all_links=[]): # ignore_fn=lambda x: False,

    re_word = key.replace('.', '\.')
    re_capture = u"([^\w\-/äöüßÄÖÜ])(%s)([^\w\-/äöüßÄÖÜ])" % re_word
    highlighting = False

    if attributes:
        if 'case-sensitive' in attributes:
            if attributes['case-sensitive'] == False:
                re_capture = u"([^\w\-/äöüßÄÖÜ])(%s|%s|%s)([^\w\-/äöüßÄÖÜ])" % (
                    re_word, re_word.lower(), re_word.title())
        if 'highlighting' in attributes:
            highlighting = True

    if highlighting:
        # replace strings with string
        for tail in [False, True]:
            thistext = element.tail if tail else element.text
            if thistext != None:
                iterator = re.finditer(re_capture, " %s " % thistext)
                iterator = reversed(list(iterator))
                final, lastend = [], 0

                pre = attributes['highlighting'].get('pre', '-set-pre-marker-')
                post = attributes['highlighting'].get('post', '-set-post-marker-')
                if iterator:
                    for match in iterator:
                        start, end = match.span()
                        # check if there is not a starting markup in the first
                        # part already ...no markup inside of the same markup
                        pre_c1 = thistext[:start].count(pre)
                        post_c1 = thistext[:start].count(post)
                        if pre_c1 == post_c1:
                            count += 1
                            thistext = "%s%s%s%s%s" % (thistext[:start],
                                pre, match.groups()[1], post,
                                thistext[end-2:])
                        if tail:
                            element.tail = thistext
                        else:
                            element.text = thistext

    else:
        # replace string with links in element
        final, lastend= [], 0

        if element.text:

            iterator = re.finditer(re_capture, " %s " % element.text)
            allitems = [(match.start(), match.end(), match) for match in iterator]
            if allitems:

                chain, lastend, lastrest = [], 0, None
                for i,(start,end,match) in enumerate(allitems):
                    before = element.text[lastend:start]
                    chain.append((before, match))
                    lastend = end-2
                    lastrest = element.text[lastend:]

                chain.append((lastrest, match))
                chain.reverse()

                for i,(after,match) in enumerate(chain):
                    newlink = get_newlink(key, value, key_attributes,
                        replacement_fn, match, attributes)
                    if element.tag != newlink.tag:
                        newlink.tail = after
                        if i < len(chain)-1:
                            count += 1
                            element.insert(0, newlink)
                        else:
                            element.text = after

        if element.tail:

            iterator = re.finditer(re_capture, " %s " % element.tail)
            allitems = [(match.start(), match.end(), match) for match in iterator]
            if allitems:
                chain, lastend, lastrest = [], 0, None
                for i,(start,end,match) in enumerate(allitems):
                    before = element.tail[lastend:start]
                    chain.append(before)
                    lastend = end-2
                    lastrest = element.tail[lastend:]

                chain.append(lastrest)
                chain.reverse()
                element.tail = ''

                for i,textbefore in enumerate(chain):
                    if textbefore:
                        if i == 0:
                            element.tail = textbefore
                            continue
                        newlink = get_newlink(key, value, key_attributes,
                            replacement_fn, match, attributes)
                        element.addnext(newlink)
                        count += 1
                        if i <= len(chain)-1:
                            element.tail = textbefore
    return count


def replace_token(content, key, value, key_attributes, replacement_fn,
    count=0, replaces=None, link_format=None):
    """
    Takes content as a string, a match to replace and the replacement.

    Updates content with all matches of the "key" variable and surrounds them
    with an "a" tag with a class "in-text-link" and a href of the "value"
    variable. The key string is not case sensitive and it will only surround
    matches of the key string that are not surround by other letters, it tries
    to match whole words.

    Ruturns a tuple with the updated content and the number of replacements
    made.

    """
    root = to_tree(content)
    count = 0
    for element in root.iter():
        count = replace_in_element( count,
                                    element,
                                    key,
                                    value,
                                    key_attributes,
                                    replacement_fn,
                                    replaces=replaces,
                                    # ignore_fn=ignore_fn,
                                    attributes=link_format)

        if replaces and count == replaces:
            return (from_tree(root), count)

    return (from_tree(root), count)


def add_links(text, links, **kwargs):
    """
    Takes html and a dictionary of words to highlight and links. Surrounds
    the matched words with a specified html element - by default a link.
    """
    replacement_format = link_fn
    counts = []
    append = counts.append

    for link in links:
        key = link.keys()[0]
        link_key = link[key]

        text, count = replace_token(
            text,
            key,
            link_key.get('value', key),
            link_key.get('attributes', []),
            replacement_format,
            replaces=kwargs.get('replaces_per_item', None),
            link_format=kwargs.get('markup_format', None),
            )
        append((key, count))

    return text, counts


# if __name__ == "__main__":
#     pass
