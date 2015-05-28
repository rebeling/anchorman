Introduction
==============

Anchorman uses three things: a text, some links and a markup
specification. It will iterate the text parse [1]_ and try to apply
the links.

Markup specification define your strategy for replacing the elements.
One option is to create a tag of a word and the other is to highlight it.

.. [1] the text will be parsed in to an lxml object for processing


Getting started
----------------

.. code-block:: python

    >>> import anchorman
    >>> text = "The quick brown fox jumps over the lazy dog."
    >>> links = [{'fox': {'value': '/wiki/fox'}},
                 {'dog': {'value': '/wiki/dog'}}]
    >>> a = anchorman.add(text, links)
    >>> a.result
    The quick brown <a href="/wiki/fox" class="anchorman">fox</a> jumps
    over the lazy <a href="/wiki/dog" class="anchorman">dog</a>.


Command replacements
--------------------
The following **keyword arguments** configure anchormans general
replacement behavior.

* **replaces_per_item** (int): Default 1
    Item in links, from first occurence on - starting left edge.

* **replaces_at_all** (int): Default infinite
    How many items will be marked at all in the text.

* **longest_match_first** (bool): Default is True. Links will be
    ordered by length and then applied. Set to False will not change
    the order you put in and follows it.

* **markup_format** (dict): specifiers the general markup,
    see next chapter for details


Markup format
++++++++++++++

The markup provides two strategies, **linking** and **highlighting**.
For links specify a tag, a value_key (attribute for item value) and a
list of attributes. The attributes will be added pairwise as
attribute=value to the tag.

.. code::

    # linking
    markup_format = {
        'tag': 'a',
        'value_key': 'href',
        'attributes': [
            ('style', 'color:blue;cursor:pointer;'),
            ('class', 'anchorman')
        ]
    }

To use **highlighting** simply add a highlighting object with pre and post
definitions. Pre and post could be everything and will be added pre and
post the match.

.. code::

    # highlighting
    markup_format = {
        'highlighting': {
            'pre': '${{',
            'post': '}}'
        }
    }

The following markup_format params hold for both strategies,
linking and highlighting.

* **case_sensitive** (bool): Default is True. If not, find the lower,
    upper and title case version of item key: fox, FOX, Fox.

* **replace_match_with_value** (bool): Default is False.
    If True, anchorman replaces the matched key in the output text.
    For example if you need an id in a template, rather then original
    term.

    .. code::

        >>> links = [{'fox': {'value': 'some-id'}}]
        >>> text = "The fox is eating chicken."
        >>> a = anchorman.add(text, links)
        >>> a.result
        The ${{some-id}} is eating chicken.


Links format
++++++++++++++

Links is a list of items. Key is the replacement to be found in
the text and its value, a dict of repl value and attributes.

Attributes will be added pairwise as attribute=value to the tag. If the
name of the attribute is already specified in the markup_format, then
markup_format attribute will be extended with the value of the item.

.. code::

    >>> links = [{
            'red fox': {
                'value': '/wiki/redfox',
                'attributes': [
                    ('class', 'animal'),
                    ('style', 'font-size:23px;background:red;'),
                    ('title', 'Fix und Foxi')
                ]
            }
        }]

    # the markup_format from above augmented with this link data
    <a ... class="anchorman animal" style="color:blue;cursor:pointer;
    font-size:23px;background:red;" ... > ... </a>


Removal
---------

Items to be removed will be identified by xpath expression.

The information from markup_format will be used to create the
rm selector. If you need to replace specific items only, provide a
selector as keyword argument to the remove function or to the
markup_format.

.. code::

    >>> selector=".//a[contains(@href, '/wiki/fox')]"
    >>> a.remove(selector=selector)

.. * **rm-identifier** Create a specific identifier per set to delete
..     its members later.


Positions
---------

If you need to know the positions of your items/links in the text. Just
call positions function on your anchorman object.

.. code::

    >>> text = "fox fox dog dog dog"
    >>> links = [{"fox": {}}]
    >>> a = add(text,links)
    >>> print a.positions()
    [('fox', (0, 3)), ('fox', (4, 7))]
