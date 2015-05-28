#!/usr/bin/env python
# encoding: utf-8

import regex as re
from lxml import etree
from tree import to_tree, from_tree
from utils import re_pattern_of


def remove_links(content, markup_format, selector='.//a[@class="anchorman"]'):
    """
    Takes a string of HTML or text and removes all the tags
    - specified by selector - and leaves their content.
    """
    if 'highlighting' in markup_format:
        # remove pre and post tags
        pre = markup_format['highlighting'].get('pre', None)
        post = markup_format['highlighting'].get('post', None)
        if pre and post:
            return content.replace(pre, '').replace(post, '')
        return content
    else:
        # remove by selector
        root = to_tree(content)
        to_remove = root.xpath(selector)
        for element in to_remove:
            element.tag = "to-remove"
            etree.strip_tags(root, "to-remove")
        return from_tree(root)


def link_fn(value, key_attributes, match, attributes=None):
    # print 'link_fn', value, key_attributes, match, attributes
    # apply special attributes for every item to global attributes or iteself
    if attributes is None:
        attributes = {}
    ka_applied, ka = [], {}
    if key_attributes:
        ka = dict(key_attributes)

    element = etree.Element(attributes.get('tag', 'a'))
    value_key = attributes.get('value_key', 'href')

    vk = attributes.get("replace_match_with_value", False)

    if vk:
        element.text = value
    else:
        element.text = match.groups()[1]
        element.attrib[value_key] = value

    for (k, v) in attributes.get('attributes', [("class", "anchorman")]):
        if k in ka:
            v = "%s %s" % (v, ka[k])
            ka_applied.append(k)
        element.attrib[k] = v

    rest = list(set(ka.keys()) - set(ka_applied))
    if rest:
        for r in rest:
            element.attrib[r] = ka[r]

    return element


def finditer_result(element_sth, replaces, re_capture):
    iterator = re.finditer(re_capture, "{}".format(element_sth),
                           overlapped=True)
    return list(iterator)[:replaces] if replaces else list(iterator)


def calculate_hl(count, element, re_capture, replaces_per_item, value,
                 pre, post, rplc_match_with_value):

    for tail in [False, True]:
        thistext = element.tail if tail else element.text

        if thistext is not None:
            iterator = reversed(finditer_result(thistext,
                                                replaces_per_item,
                                                re_capture))

            if iterator:
                for match in iterator:
                    start, end = match.span()
                    groups = match.groups()
                    # check if there is not a starting markup
                    # in the first part already ...no markup
                    # inside of the same markup

                    pre_c1 = thistext[:start].count(pre)
                    post_c1 = thistext[:start].count(post)

                    # replace_match_with_value
                    repl = value if rplc_match_with_value else groups[1]

                    if pre_c1 == post_c1:
                        count += 1
                        before, after = len(groups[0]), len(groups[2])

                        thistext = "{}{}{}{}{}".format(
                            thistext[:start+before], pre, repl, post,
                            thistext[end-after:])

                    if tail:
                        element.tail = thistext
                    else:
                        element.text = thistext
    return count


def get_chain(allitems, element, tail_mode=True):
    lastend, lastrest, match = 0, None, None
    chain = []
    chain_append = chain.append
    this = element.tail if tail_mode else element.text

    for match in allitems:
        start, end = match.span()
        before = this[lastend:start]
        chain_append((before, match))
        lastend = end
        lastrest = this[lastend:]
    chain_append((lastrest, match))
    chain.reverse()

    return chain


def calculate_el(count, attributes, element, replaces_per_item,
                 re_capture, replacement_fn, value, key_attributes):

    if element.text:
        allitems = finditer_result(element.text,
                                   replaces_per_item,
                                   re_capture)
        if allitems:
            chain = get_chain(allitems, element, tail_mode=False)
            for i, (after, match) in enumerate(chain):
                newlink = replacement_fn(value, key_attributes,
                                         match, attributes=attributes)
                if element.tag != newlink.tag:
                    groups = match.groups()
                    newlink.tail = "{}{}".format(groups[2], after)

                    if i < len(chain)-1:
                        element.insert(0, newlink)
                        count += 1
                    else:
                        element.text = "{}{}".format(after, groups[0])

    if element.tail:
        allitems = finditer_result(element.tail,
                                   replaces_per_item,
                                   re_capture)
        if allitems:
            chain = get_chain(allitems, element, tail_mode=True)
            element.tail = ''

            for i, (textbefore, match) in enumerate(chain):

                groups = match.groups()
                if i == 0:
                    element.tail = groups[2] + textbefore
                    continue

                newlink = replacement_fn(value,
                                         key_attributes,
                                         match,
                                         attributes=attributes)
                element.addnext(newlink)

                count += 1
                if i <= len(chain)-1:
                    element.tail = textbefore + groups[0]
    return count


def replace_in_element(count, element, key, value, key_attributes,
                       replacement_fn, attributes, replaces_per_item):

    highlighting = attributes.get('highlighting', {})
    case_sens = attributes.get('case_sensitive', True)
    _, re_capture = re_pattern_of(key, case_sensitive=case_sens)
    rplc_match_with_value = attributes.get("replace_match_with_value",
                                           False)

    if highlighting:
        # replace strings with string
        count = calculate_hl(count,
                             element,
                             re_capture,
                             replaces_per_item,
                             value,
                             highlighting.get('pre', '-set-pre-marker-'),
                             highlighting.get('post', '-set-post-marker-'),
                             rplc_match_with_value)
    else:
        # replace string with links in element
        count = calculate_el(count,
                             attributes,
                             element,
                             replaces_per_item,
                             re_capture,
                             replacement_fn,
                             value,
                             key_attributes)
    return count


def replace_token(content, key, value, key_attributes, replacement_fn,
                  replaces_per_item, link_format, count=0):
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
        count = replace_in_element(count,
                                   element,
                                   key,
                                   value,
                                   key_attributes,
                                   replacement_fn,
                                   link_format,
                                   replaces_per_item
                                   # ignore_fn=ignore_fn
                                   )

        if replaces_per_item and count == replaces_per_item:
            return (from_tree(root), count)

    return (from_tree(root), count)


def add_links(text, links, replaces_per_item=None, replaces_at_all=None,
              markup_format=None):
    """
    Takes html and a dictionary of words to highlight and links. Surrounds
    the matched words with a specified html element - by default a link.
    """
    replacement_format = link_fn
    counts = []
    append = counts.append
    total_count = 0

    for link in links:
        key = link.keys()[0]
        link_key = link[key]

        text, count = replace_token(
            text,
            key,
            link_key.get('value', key),
            link_key.get('attributes', []),
            replacement_format,
            replaces_per_item,
            markup_format)
        append((key, count))

        total_count += count
        if total_count >= replaces_at_all:
            break

    return text, counts
