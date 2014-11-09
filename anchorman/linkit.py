import re
from lxml import etree
from functools import partial
from tree import to_tree, from_tree, update_text, update_tail


def create_link(term, value, match):
    """
    Create an lxml anchor element
    """
    element = etree.Element('a')
    element.attrib["class"] = "anchorman"
    element.attrib["href"] = value
    element.text = match
    return element


def is_link(element):
    """
    Return true if the element is a link
    """
    return element is not None and element.tag == "a"


def remove_elements(content, selector):
    """
    Takes a string of HTML or text and removes all the tags matching the
    selector.

    Returns a new string.
    """
    root = to_tree(content)

    to_remove = root.xpath(selector)
    for element in to_remove:
        element.tag = "deleted"

    etree.strip_tags(root, "deleted")

    return from_tree(root)


def search_text(string, word):
    """
    Takes a string of text and searches for a matching word.

    * Attempts to ignore all punctuation to only.
    * Matches whole words
    * Ignores case

    Returns a tuple of the text before the match, the match and after the match
    if a word exists or returns None is no match is found.
    """
    re_word = u"".join([u"[%s%s]" % (c.upper(), c.lower())
                        for c in list(word)])
    re_capture = u"(\W)(%s)([^\w\-])" % re_word
    match = re.search(re_capture, " %s " % string)
    if match:
        offset = match.start()
        pre_part = string[:offset]
        matched_part = match.groups()[1]
        post_part = string[offset + len(matched_part):]
        return (pre_part, matched_part, post_part)


def replace_in_element(element, search_word,
                       replace=create_link,
                       ignore=is_link,
                       search=search_text):
    """
    Recursively search `element` and its children for text containing the
    `search_word`. The first instance of the word that is in an element that
    doesn't return true if applied to the `ignore` function is removed and an
    element created by `replace` is inserted in its place.

    The `search` function is applied to the text part of elements. It must
    return a tuple (text_before_match, matched_text, text_after_match) or None.

    The `replace` function is applied with the matching `search_word` as an
    argument. It is expected to return an lxml Element.

    The `ignore` function is applied with the containing element as an
    argument, if the function returns True that element isn't searched, however
    the ignore function is still applied to each child element.
    """

    # Search in text
    if not ignore(element):
        text = element.text
        match = search(text, search_word)
        if match:
            pre_str, matched, post_str = match
            new_element = replace(matched)
            update_text(element, pre_str, new_element, post_str)
            return True

    # Search child elements
    for child in element.iterchildren():
        result = replace_in_element(child, search_word, replace, ignore)
        if result:
            return True

    # Search tail text
    if not ignore(element.getparent()):
        text = element.tail
        match = search(text, search_word)
        if match:
            pre_str, matched, post_str = match
            new_element = replace(matched)
            update_tail(element, pre_str, new_element, post_str)
            return True

    return False


def replace_token(content, key, make_element, ignore_element):
    """
    Take content as a string and search

    Updates content with all matches of the "key" variable and surrounds them
    with an element created by make_element. The key string is not case
    sensitive and it will only surround matches of the key string that are not
    surround by other letters, it tries to match whole words.

    Ruturns a tuple with the updated content and the number of replacements
    made.

    """

    root = to_tree(content)
    updated = replace_in_element(root, key, make_element, ignore_element)
    return (from_tree(root), updated)


def add_in_text_links(content, links):
    """
    Takes content and a dictionary of words to highlight and links. Surrounds
    the matched words are replaced with an "a" tag with the link.
    """
    return reduce(lambda acc, val: replace_token(acc, val[0],
                                                 partial(create_link, val[0],
                                                         val[1]),
                                                 is_link)[0],
                  dict(links).iteritems(), content)

if __name__ == "__main__":
    text = '<p><br/>Fox.</p>'
    #print replace_token(text, "Fox", "hello", link_fn)
