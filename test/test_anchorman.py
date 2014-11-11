#!/usr/bin/env python
# encoding: utf-8
import pytest
import anchorman


def link(key):
    link_format = u"<a class=\"anchorman\" href=\"%s\">%s</a>"
    return link_format % (links[key.lower()], key)


links = {
    u"fox": "a red animal",
    u"dog": "not a fox",
    u"föx": "a unicode red animal"
}

update_pairs = [
    (u"the unicode föx", u"the unicode %s" % link(u"föx")),
    (u"<p><b>fox</b></p>fox", u"<p><b>%s</b></p>%s" % (link("fox"),link("fox"))),
    (u'<a/>dog', u'<a/>%s' % link("dog")),
    (u'<a/>dog.', u'<a/>%s.' % link("dog")),
    (u'<a href="a red animal">rat</a> dog', u'<a href="a red animal">rat</a> %s' % link("dog")),
    (u'<a href="a red animal">rat</a>!dog', u'<a href="a red animal">rat</a>!%s' % link("dog")),
    (u"quick brown fox jumped over the lazy cat", u"quick brown %s jumped over the lazy cat" % link("fox")),
    (u"quick brown cat jumped over the lazy dog", u"quick brown cat jumped over the lazy %s" % link("dog")),
    (u"quick brown fox jumped over the lazy dog", u"quick brown %s jumped over the lazy %s" % (link("fox"), link("dog"))),
    (u"<b>fox</b><b>fox</b>", u"<b>%s</b><b>%s</b>" % (link("fox"),link("fox"))),
    (u"is foxdog a dogfox?", u"is foxdog a dogfox?"),
    (u"fox", u"%s" % link("fox")),
    (u"fox and fox", u"%s and fox" % link("fox")),
    (u"Is it a dog? No, it's fox!", u"Is it a %s? No, it's %s!" % (link("dog"), link("fox"))),
    (u'<p class="fox">fox</p>', u'<p class="fox">%s</p>' % link("fox")),
    (u"<p>fox</p>", u"<p>%s</p>" % link("fox"))

    # do we really want this or specify: ['fox', 'Fox', 'FOX']
    # (u"the captial FOX is shouty", u"the captial fox is shouty" % link("FOX")),
]

update_pairs_with_kwargs = [
    # todo: replace the first occurence first and so on
    (u"<p><b>fox</b></p>fox and fox", u"<p><b>fox</b></p>%s and fox" % link("fox")),
]

@pytest.fixture(scope='module', params=update_pairs)
def add_links(request):
    original, with_links = request.param
    return (with_links, anchorman.add_links(original, links))


@pytest.fixture(scope='module', params=update_pairs_with_kwargs)
def add_links_with_kwargs(request):
    original, with_links = request.param
    return (with_links, anchorman.add_links(original, links, replaces=1))


@pytest.fixture(scope='module', params=update_pairs)
def remove_links(request):
    original, with_links = request.param
    return (original, anchorman.remove_links(with_links))


def test_add_links(add_links):
    (expected, updated) = add_links
    assert expected == updated.text


def test_add_links_with_kwargs(add_links_with_kwargs):
    (expected, updated) = add_links_with_kwargs
    assert expected == updated.text


def test_remove_links(remove_links):
    (expected, updated) = remove_links
    assert expected == updated
