#!/usr/bin/env python
# encoding: utf-8

import regex as re
from lxml import etree
from tree import to_tree, from_tree


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
            if rmtuple:
                selector = './/%s[@%s="%s"]' % (tag, rmtuple[0], rmtuple[1])
        # else do not overwrite the default self.selector
        new_link_format = {
            'tag': link_format.get('tag', 'a'),
            'value_key': link_format.get('value_key', 'href'),
            'attributes': link_format.get('attributes', [])
            }
    return new_link_format, selector


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


def finditer_result(element_sth, replaces, re_capture):
    iterator = re.finditer(
        re_capture, "{}".format(element_sth), overlapped=True)
    if replaces:
        return list(iterator)[:replaces]
    else:
        return list(iterator)

def calculate_hl(count, element, re_capture, replaces_per_item, value, pre, post, replace_match_with_value):

    for tail in [False, True]:
        thistext = element.tail if tail else element.text
        if thistext is not None:
            iterator = reversed(finditer_result(thistext, replaces_per_item, re_capture))
            lastend = 0
            if iterator:
                for match in iterator:
                    start, end = match.span()
                    # check if there is not a starting markup
                    # in the first part already ...no markup
                    # inside of the same markup
                    add2start = len(match.groups()[0])
                    sub2end = len(match.groups()[2])
                    pre_c1 = thistext[:start].count(pre)
                    post_c1 = thistext[:start].count(post)
                    # replace_match_with_value
                    repl = value if replace_match_with_value else match.groups()[1]
                    if pre_c1 == post_c1:
                        count += 1
                        thistext = "{}{}{}{}{}".format(
                            thistext[:start+add2start],
                            pre, repl, post,
                            thistext[end-sub2end:])
                    if tail:
                        element.tail = thistext
                    else:
                        element.text = thistext
    return count


def calculate_el(count, attributes, element, replaces_per_item,
    re_capture, replacement_fn, value, key_attributes):

    lastend = 0

    if element.text:
        allitems = finditer_result(element.text, replaces_per_item, re_capture)
        if allitems:
            chain, lastend, lastrest = [], 0, None

            for i, match in enumerate(allitems):
                start, end = match.span()
                before = element.text[lastend:start]
                chain.append((before, match))
                lastend = end
                lastrest = element.text[lastend:]

            if lastrest:
                chain.append((lastrest, match))

            chain.reverse()

            for i, (after, match) in enumerate(chain):
                newlink = replacement_fn(value,
                                         key_attributes,
                                         match,
                                         attributes=attributes)

                if element.tag != newlink.tag:
                    newlink.tail = "{}{}".format(
                        match.groups()[2], after)

                    if i < len(chain)-1:
                        count += 1
                        element.insert(0, newlink)
                    else:
                        element.text = "{}{}".format(
                            after, match.groups()[0])

    if element.tail:
        allitems = finditer_result(element.tail, replaces_per_item, re_capture)
        if allitems:
            chain, lastend, lastrest = [], 0, None

            for i, match in enumerate(allitems):
                start, end = match.span()
                before = element.tail[lastend:start]
                chain.append(before)
                lastend = end
                lastrest = element.tail[lastend:] # + matchedafter

            chain.append(lastrest)
            chain.reverse()
            element.tail = ''

            for i, textbefore in enumerate(chain):

                if i == 0:
                    element.tail = match.groups()[2] + textbefore
                    continue

                newlink = replacement_fn(value,
                                         key_attributes,
                                         match,
                                         attributes=attributes)
                element.addnext(newlink)

                count += 1
                if i <= len(chain)-1:
                    element.tail = textbefore + match.groups()[0]
    return count


def replace_in_element(count, element, key, value, key_attributes,
    replacement_fn, attributes, replaces_per_item): # replaces,  ignore_fn=lambda x: False,

    highlighting = attributes.get('highlighting', {})
    case_sens = attributes.get('case_sensitive', True)
    re_word, re_capture = re_pattern_of(key, case_sensitive=case_sens)
    replace_match_with_value = attributes.get("replace_match_with_value", False)

    if highlighting:
        # replace strings with string
        count = calculate_hl(count,
                             element,
                             re_capture,
                             replaces_per_item,
                             value,
                             highlighting.get('pre', '-set-pre-marker-'),
                             highlighting.get('post', '-set-post-marker-'),
                             replace_match_with_value)
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
