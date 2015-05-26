Usage
=====
Anchorman uses three things: a text, some links and a markup specification. It will iterate the text parse[1] and try to apply the links.

Markup specification define the strategy. One option is to create a tag of a word and the other is to highlight it.

[1] the text will be parsed in to an lxml object for processing


General Params
--------------
The following **keyword arguments** configure anchormans
general behavior.

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
+++++++++++++

The markup provides two strategies, **linking** and **highlighting**.
For links specify a tag, a value_key (attribute for item value) and a
list of attributes. The attributes will be added pairwise as
attribute=value to the tag.

.. code::

    >>> markup_format = {
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

    >>> markup_format = {
            'highlighting': {
                'pre': '${{',
                'post': '}}'
            }
        }

The following params hold for both strategies, linking and highlighting.

* **case_sensitive** (bool): Default is True. Set to False,
    it is possible to find the lower, upper and title case version of
    item key: fox, FOX, Fox. ...to be improved.

* **replace_match_with_value** (bool): Default is False.
    Set to True, the param allows you to replace the matched key in the output text. For example if you need an id in a template, rather then original term.

    .. code::

        {'fox': {'value': 'some-id'}}
        "The fox is eating chicken."
        Result: The ${{some-id}} is eating chicken.


Items/Links format
------------------

The links will be list of items. Key is the replacement to be find in
text and its value is a dict of value and attributes.

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



Links with specific attributes
------------------------------

Define general attribute value pairs on markup_format level and more specific attributes at the level of each link element.

.. code::

    >>> links = [{
            'red fox': {
                'value': '/redfox',
                'attributes': [
                    ('class', 'animal'),
                    ('style', 'font-size:23px;background:red'),
                    ('title', 'Fix und Foxi')
                ]
            }
        }]
    >>> a = anchorman.add(text, links, markup_format=markup_format)
    The quick brown fox jumps over the lazy dog while the <a href="/redfox"
    style="color:blue;cursor:pointer; font-size:23px;background:red"
    class="anchorman animal" title="Fix und Foxi">red fox</a> sleeps.


Highlighting context
--------------------

Instead of creating tags, you define pre- and post-context for highlighting.
If highlighting is specified in the markup_format, the link key will be marked
in text. Usage e.g. variables in templates or simple tags (em, b).

.. code::

    >>> links = [{'fox': {}}]
    >>> markup_format = {
            'highlighting': {
                'pre': '${{',
                'post': '}}'
            }
        }
    >>> a = anchorman.add(text, links, markup_format=markup_format)
    >>> print a
    The quick brown ${{fox}} jumps over the lazy dog while the red
    ${{fox}} sleeps.



Removal
---------

.. code::

    rm-identifier: create a specific identifier per set to delete them later


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
