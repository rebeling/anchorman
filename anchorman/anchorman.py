#!/usr/bin/env python
# -*- coding: utf-8 -*-
from linkit import add_links
from linkit import finditer_result
from linkit import remove_links
from utils import linker_format
from utils import re_pattern_of
from utils import sort_longest_match_first
from utils import validate_input


class Anchorman(object):
    """Main module interface object for add and remove annotations.

    Args:
        text (string, optional): The first parameter.

        links (list, optional): The second parameter.
            Second line of description should be indented.


    Keyword Args:

        selector (string)

        replaces_per_item (int): Default 1

        replaces_at_all (int): Default 5555555

        longest_match_first (bool): Default True


    Markup_format in kwargs will update selector when processed.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the class with data from args and kwargs

        """
        self.text = None
        self.links = None
        if args:
            self.text = args[0]
            self.links = args[1]
        self.selector = kwargs.get('selector', './/a')
        self.replaces_per_item = kwargs.get('replaces_per_item', 1)
        self.replaces_at_all = kwargs.get('replaces_at_all', 5555555)
        self.longest_match_first = kwargs.get('longest_match_first', True)
        self._markup_format = {'tag': 'a', 'value_key': 'href'}
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
        """Markup format updates link and selector"""
        _, _selector = linker_format(markup_format)
        if _selector:
            self.selector = _selector
        if markup_format.get('selector', None):
            self.selector = markup_format['selector']
        self._markup_format = markup_format

    def _update_data(self, *args, **kwargs):

        if args:
            try:
                if 'remove' in kwargs:
                    self.text = args[0]
                else:
                    self.text, self.links = args[0], args[1]
            except ValueError, e:
                raise "Args not specified correctly: %s" % e

        if 'replaces_per_item' in kwargs:
            self.replaces_per_item = kwargs['replaces_per_item']

        if 'markup_format' not in kwargs:
            self.markup_format = self.markup_format
        else:
            self.markup_format = kwargs['markup_format']

    def add(self, *args, **kwargs):
        """Add links to text.

        Text and links can be initialized on class level, but also
        reset in here as args.

        Args:
            text: The first parameter.
            links: The second parameter.

        Returns:
            result (String): the enriched text.
        """
        self._update_data(*args, **kwargs)
        if self.longest_match_first:
            self.links = sort_longest_match_first(self.links)

        result = add_links(self.text,
                           self.links,
                           replaces_per_item=self.replaces_per_item,
                           replaces_at_all=self.replaces_at_all,
                           markup_format=self.markup_format)

        self.result, self.counts = result
        return self.result

    def remove(self, *args, **kwargs):
        """Remove links/markup from text based on markup_format.

        Returns:
            result (String): the cleared text.
        """
        kwargs['remove'] = True
        self._update_data(*args, **kwargs)
        if kwargs.get('selector', None):
            self.selector = kwargs['selector']
        self.result = remove_links(kwargs.get('text', self.result),
                                   self.markup_format,
                                   selector=self.selector)
        return self.result

    def positions(self, **kwargs):
        """Get positions of all links in text.

        Returns:
            result (List): list of tuples (match, positions) in text.
        """
        allkeys = map(lambda a: a.keys()[0], self.links)
        result = []
        text = "{}".format(self.text)

        cs = kwargs.get('case_sensitive',
                        self.markup_format.get('case_sensitive', True))
        _, re_capture = re_pattern_of(allkeys, case_sensitive=cs)
        r = finditer_result(text, None, re_capture)
        for match in r:
            st, en = match.span()
            gr = match.groups()
            st += len(gr[0])
            en -= len(gr[2])
            # result.append((key, (st, en), match.groups()[1]))
            result.append((match.groups()[1], (st, en)))
        return result


def add(text, links, **kwargs):
    """Call class on module level, initialize and return the class.

    Operate on this object instead of the class directly for simplicity.
    If text and links are provided apply them. The returned object
    contains result then already.

    Examples:
        Use it like this::

            import anchorman
            a = anchorman.add(text, links)

    Args:
        text: The first parameter.
        links: The second parameter.

    Returns:
        anchorman (class): the class object with added markup.

    """
    success, values = validate_input((text, links))
    if success:
        text, links = values
    else:
        raise ValueError(values)

    a = Anchorman(text, links, **kwargs)
    a.add()
    return a
