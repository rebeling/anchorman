# -*- coding: utf-8 -*-
import pytest
from lxml import etree
from tagger.tagger import remove_elements, \
    add_in_text_links, search_text

selector = './/a[@class="in-text-link"]'


def link(key):
    link_format = u"<a class=\"in-text-link\" href=\"%s\">%s</a>"
    return link_format % (links[key.lower()], key)

links = {
    u"fox": "a red animal",
    u"dog": "not a fox",
    u"föx": "a unicode red animal"
}

search_tests = [
    (u"fox", u"fox", (u"", u"fox", u"",)),
    (u"fox", u"Fox", (u"", u"Fox", u"")),
    (u"fox", u"rabbit", None),
    (u"fox", None, None),
    (u"fox", u"The Fox Way", (u"The ", u"Fox", u" Way")),
    (u"fox", u"'fox'", (u"'", u"fox", u"'")),
    (u"fox", u"quick brown fox jumped over the lazy dog",
     ("quick brown ", "fox", " jumped over the lazy dog"))
]

update_pairs = [
    (u'<a/>dog',
     u'<a/>%s' % link("dog")),
    (u'<a href="a red animal">rat</a> dog',
     u'<a href="a red animal">rat</a> %s' % link("dog")),
    (u'<a href="a red animal">rat</a>!dog',
     u'<a href="a red animal">rat</a>!%s' % link("dog")),
    (u"quick brown fox jumped over the lazy cat",
     u"quick brown %s jumped over the lazy cat" % link("fox")),
    (u"quick brown cat jumped over the lazy dog",
     u"quick brown cat jumped over the lazy %s" % link("dog")),
    (u"quick brown fox jumped over the lazy dog",
     u"quick brown %s jumped over the lazy %s" % (link("fox"), link("dog"))),
    (u"<b>fox</b><b>fox</b>",
     u"<b>%s</b><b>fox</b>" % link("fox")),
    (u"is foxdog a dogfox?",
     u"is foxdog a dogfox?"),
    (u"the unicode föx",
     u"the unicode %s" % link(u"föx")),
    (u"fox",
     u"%s" % link("fox")),
    (u"fox and fox",
     u"%s and fox" % link("fox")),
    (u"the captial FOX is shouty",
     u"the captial %s is shouty" % link("FOX")),
    (u"Is it a dog? No, it's fox!",
     u"Is it a %s? No, it's %s!" % (link("dog"), link("fox"))),
    (u'<p class="fox">fox</p>',
     u'<p class="fox">%s</p>' % link("fox")),
    (u"<p><b>fox</b></p>fox",
     u"<p><b>%s</b></p>fox" % link("fox")),
    (u"<p>fox</p>",
     u"<p>%s</p>" % link("fox"))
]



def link_fn(key, value, match):
    element = etree.Element('a')
    element.attrib["class"] = "in-text-link"
    element.attrib["href"] = value
    element.text = match
    return element


def ignore_fn(element):
    return False


@pytest.fixture(scope='module', params=search_tests)
def search_texts(request):
    term, text, expected = request.param
    return (expected, search_text(text, term))

@pytest.fixture(scope='module', params=update_pairs)
def add_links(request):
    original, with_links = request.param
    return (with_links, add_in_text_links(original, links))


@pytest.fixture(scope='module', params=update_pairs)
def remove_links(request):
    original, with_links = request.param
    return (original, remove_elements(with_links, selector))


def test_add_links(add_links):
    (expected, updated) = add_links
    assert expected == updated


def test_remove_links(remove_links):
    (expected, updated) = remove_links
    assert expected == updated


def test_search_text(search_texts):
    (expected, actual) = search_texts
    assert expected == actual
