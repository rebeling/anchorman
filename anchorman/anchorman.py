#!/usr/bin/env python
# -*- coding: utf-8 -*-
from linkit import linker_format
from linkit import add_links
from linkit import remove_links
from utils import sort_for_longest_match_first
from utils import validate_input


class Anchorman(object):
    """Create the main object for the add_links request. """

    def __init__(self, *args, **kwargs):
        """Initialize the class with data from args and kwargs """
        self.text = args[0]
        self.links = args[1]
        self.markup_format = kwargs.get('markup_format',
                                        {'tag': 'a', 'value_key': 'href'})
        self.replaces_per_item=kwargs.get('replaces_per_item', None)
        self.link_format = kwargs.get('link_format', {})
        self.selector = './/a'
        self.set_link_format()
        self.result = None
        self.counts = None

    def __str__(self):
        return self.result

    def set_link_format(self):
        """Set the markup format from self.markup_format

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
        _link_format, _selector = linker_format(self.markup_format)
        if _link_format:
            self.link_format = _link_format
        if _selector:
            self.selector = _selector

    def add(self, *args, **kwargs):
        """Augment text with the items of links

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
        """
        if args:
            self.text, self.links = args[0], args[1]

        if 'replaces_per_item' not in kwargs:
            kwargs['replaces_per_item'] = self.replaces_per_item
        if 'markup_format' not in kwargs:
            kwargs['markup_format'] = self.markup_format
        else:
            self.markup_format = kwargs['markup_format']

        self.set_link_format()
        kwargs['link_format'] = self.link_format

        self.result, self.counts = add_links(
            self.text,
            sort_for_longest_match_first(self.links),
            **kwargs)
        return self.result

    def remove(self, *args, **kwargs):
        """Remove the markup driven by actual/latest markup_format """
        self.markup_format = kwargs.get('markup_format', self.markup_format)
        self.set_link_format()

        self.result = remove_links(
            kwargs.get('text', self.result),
            selector=self.selector,
            markup_format=self.markup_format)


def add(*args, **kwargs):
    """Call class on module level, initialize like this, get back the
        class and operate on this object instead of the class directly

        import anchorman
        a = anchorman.add(text, links)
    """
    success, values = validate_input(args)
    if success:
        text, links = values
    else:
        raise ValueError(values)

    a = Anchorman(text, links, **kwargs)
    a.add()
    return a


# if __name__ == '__main__':

#     links = [{'fox': {'value': '/wiki/fox'}}, {'dog': {'value': '/wiki/dog'}}]
#     text = "The quick brown fox jumps over the lazy <br> dog."

#     a = add(text, links)

#     a = add(text, links)
#     print a
#     a.remove()
#     print a
