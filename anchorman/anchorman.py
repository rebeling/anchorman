#!/usr/bin/env python
# -*- coding: utf-8 -*-
from linkit import linker_format
from linkit import add_links
from linkit import remove_links
from utils import sort_longest_match_first
from utils import validate_input


class Anchorman(object):
    """
    Anchorman is the basic API for the linkit request. Beside text and
    links, use markup_format and replaces_per_item to describe the core
    functionality.

    The links will be specified as a list of dicts. Dicts key will be
    the string in the original text to be replaced/augmented.

    links = [
        {'red fox': {
            'value': '/redfox',
            # add or augment the general attributes (see markup)
            # with more specific or extra attribute, value pairs
            'attributes': [
                ('class', 'animal'),
                ('style', 'font-size:23px;background:red'),
                ('title', 'The red fox is red')
                ]
            }
        },
        {'green hornet': {
            ...
        }, ...
    ]

    The markup_format provides two options:

    1. link format
    2. context highlighting

    markup_format = {

        'tag': 'a',
        'value_key': 'href', # attribute for the value (see links in add)
        'attributes': [
            ('style', 'color:blue;cursor:pointer;'),
            ('class', 'anchorman')
            ],
        'rm-identifier': 'anchorman-link', # identifier for specific rm

        # --- * ---
        # or highlight the target with a pre- and postfix
        'highlighting': {
            'pre': '${{',
            'post': '}}'
            },

        # --- * ---
        'case-sensitive': False, # works for both, default is True
    }
    """

    def __init__(self, *args, **kwargs):
        """Initialize the class with data from args and kwargs """
        self.text = None
        self.links = None
        if args:
            self.text = args[0]
            self.links = args[1]
        self.selector = './/a'
        self.replaces_per_item=None
        self._markup_format={'tag': 'a', 'value_key': 'href'}
        self._update_data(**kwargs)
        self.result = None
        self.counts = None

    def __str__(self):
        if self.result:
            return self.result
        else:
            return "%s" % self.__class__

    @property
    def markup_format(self):
        return self._markup_format

    @markup_format.setter
    def markup_format(self, markup_format):
        """Markup format updates link and selector """
        _, _selector = linker_format(markup_format)
        if _selector:
            self.selector = _selector
        self._markup_format = markup_format

    def _update_data(self, *args, **kwargs):

        if args:
            try:
                self.text, self.links = args[0], args[1]
            except ValueError, e:
                raise "args not specified correct: %s" % e

        if 'replaces_per_item' not in kwargs:
            kwargs['replaces_per_item'] = self.replaces_per_item

        if 'markup_format' not in kwargs:
            kwargs['markup_format'] = self.markup_format
            self.markup_format = self.markup_format
        else:
            self.markup_format = kwargs['markup_format']

    def add(self, *args, **kwargs):
        """
        Text and links could be set in the class already, relax we check
        the args again - may the class vars should be reset here.
        """
        self._update_data(*args, **kwargs)
        result = add_links(self.text,
                           sort_longest_match_first(self.links),
                           replaces_per_item=self.replaces_per_item,
                           markup_format=self.markup_format)

        self.result, self.counts = result
        return self.result

    def remove(self, *args, **kwargs):
        """
        Remove the markup driven by actual/latest markup_format
        """
        self._update_data(*args, **kwargs)
        self.result = remove_links(kwargs.get('text', self.result),
                                   self.markup_format,
                                   selector=self.selector)


def add(text, links, **kwargs):
    """
    Call class on module level, initialize like this, get back the
    class and operate on this object instead of the class directly

    import anchorman
    a = anchorman.add(text, links)
    """
    success, values = validate_input((text, links))
    if success:
        text, links = values
    else:
        raise ValueError(values)

    a = Anchorman(text, links, **kwargs)
    a.add()
    return a


# if __name__ == '__main__':

#     # b = Anchorman()
#     links = [{'fox': {'value': '/wiki/fox'}}, {'dog': {'value': '/wiki/dog'}}]
#     text = "The quick brown fox jumps over the lazy <br> dog."
#     a = add(text, links)
#     print a
#     a.remove()
#     print a
