#!/usr/bin/env python
# -*- coding: utf-8 -*-

from linkit import linker_format
from linkit import add_links
from linkit import remove_links
from utils import sort_for_longest_match_first




class Anchorman(object):
    """
    Create the main object for the add_links request.
    """

    def __init__(self, *args, **kwargs):
        self.markup_format = {'tag': 'a','value_key': 'href'}
        self.link_format = {}
        self.selector = './/a'
        self.text = args[0]
        self.links = args[1]
        self.result = None
        self.counts = None
        self.set_link_format(kwargs)
        self.replaces_per_item=kwargs.get('replaces_per_item', None)

    def __str__(self):
        return self.result

    def set_link_format(self, kwargs):
        '''
        set the markup format from kwargs like this

        markup_format = {

            'tag': 'a',
            'value_key': 'href',    # attribute for the value (see links in add)
            'attributes': [
                ('style', 'color:blue;cursor:pointer;'),
                ('class', 'anchorman')
                ],
            'rm-identifier': 'anchorman-link',  # identifier for specific rm

            # --- * ---
            # or highlight the target with a pre- and postfix

            'highlighting': {
                'pre': '${{',
                'post': '}}'
                },

            # --- * ---
            'case-sensitive': False,    # works for both, default is True
        }
        '''
        markup_format = kwargs.get('markup_format', None)
        mf = self.markup_format if markup_format == None else markup_format
        self.markup_format = mf
        new_lf, selector = linker_format(self.markup_format)
        self.link_format = new_lf if new_lf else self.link_format
        self.selector = selector if selector else self.selector

    def add(self, *args, **kwargs): #links, text, **kwargs):
        '''
        augment text with the items of links
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
        '''
        if args:
            self.text = args[0]
            self.links = args[1]
        self.set_link_format(kwargs)
        kwargs['link_format'] = self.link_format
        kwargs['markup_format'] = self.markup_format
        links = sort_for_longest_match_first(kwargs.get('links', self.links))
        kwargs['replaces_per_item'] = kwargs.get('replaces_per_item', self.replaces_per_item)
        self.result, self.counts = add_links(self.text , links, **kwargs)
        return self.result

    def remove(self, *args, **kwargs):
        '''
        remove the markup driven by actual/latest markup_format
        '''
        self.set_link_format(kwargs)
        # text = args[0] if args else self.result
        text = kwargs.get('text', self.result)
        self.result = remove_links(text,
            selector=self.selector,
            markup_format=self.markup_format)


def add(text, links, **kwargs):
    '''
    call class on module level
    '''
    a = Anchorman(text, links, **kwargs)
    a.add()
    return a


# if __name__ == '__main__':

#     links = [{'fox': {'value': '/wiki/fox'}}, {'dog': {'value': '/wiki/dog'}}]
#     text = "The quick brown fox jumps over the lazy <br> dog."

#     a = add(text, links)
#     print a.result
#     a.remove()
#     print a
