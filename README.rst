============
Anchorman
============

.

Turn your text into hypertext_. With anchorman you can markup anything,
create anchors, links, annotate abbreviations or just highlight specific areas.

.. _hypertext: http://en.wikipedia.org/wiki/Hypertext

.

Example
============

.. code::

    >>> import anchorman
    >>> text = "The quick brown fox jumps over the lazy dog."
    >>> links = [{'fox': {'value': '/wiki/fox'}},
                 {'dog': {'value': '/wiki/dog'}}]
    >>> a = anchorman.add(text, links)
    >>> print a
    The quick brown <a href="/wiki/fox" class="anchorman">fox</a> jumps over
    the lazy <a href="/wiki/dog" class="anchorman">dog</a>.


See `more examples`_ section at bottom.

.

Installation
============

Install anchorman via pip, master branch status: |travis|

.. code::

    pip install anchorman

or from source code

.. code::

    git clone https://github.com/tarnacious/anchorman.git && cd anchorman
    python setup.py install

test it in a virtual environment

.. code::

    virtualenv .
    ./bin/pip install -r requirements.txt
    ./bin/py.test test

or locally

    py.test --cov=anchorman --cov-report term-missing -v -s

.. |travis| image:: https://travis-ci.org/rebeling/anchorman.svg?branch=master
    :target: https://travis-ci.org/rebeling/anchorman
    :alt: Built Status

.. _more examples:

.

More examples
==============

**Links with specific attributes**
Define general attribute value pairs on markup_format level and more specific attributes at the level of each link element.

.. code::

    >>> markup_format = {
            'tag': 'a',
            'value_key': 'href',
            'attributes': [
                ('style', 'color:blue;cursor:pointer;'),
                ('class', 'anchorman')
            ]
         }
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

.

**Highlighting context**
Highlighting a term with pre- and postfix, e.g. variables in templates or low level tags.

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

.

**Parameters**

.. code::

    markup_format: tag, value attribute or highlighting with pre- and postfix

    replaces_per_item: default is replace all occurences, otherwise int

    case-sensitive: default is True, set False to replace: Fox, fox and FOX

    rm-identifier: create a specific identifier per set to delete them later


.
Performance
===========

1000 items were processed with mean text len of 1800 characters. Same
list of links was applied and around 11 times per text items augemented.

.. code::

    # without markup
    min  0.00060 s
    max  0.00891 s
    mean 0.00152 s

    # with basic markup
    min  0.00061 s
    max  0.00929 s
    mean 0.00158 s

    # highlighting
    min  0.00057 s
    max  0.00783 s
    mean 0.00117 s

It is pretty fast already, but we need to check with larger link list and
also some other cases > this was add links only, what about remove, apply
other markup in between etc.

.
