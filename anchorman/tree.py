from lxml import etree


def to_tree(s):
    xml = "<root>%s</root>" % s
    return etree.fromstring(xml)


def from_tree(tree):
    return etree.tounicode(tree)[6:-7]


def update_tail(element, pre_string, new_element, post_string):
    element.addnext(new_element)
    element.tail = pre_string
    new_element.tail = post_string


def update_text(element, pre_string, new_element, post_string):
    element.insert(0, new_element)
    element.text = pre_string
    new_element.tail = post_string
