============
Anchorman
============

Turn your text into hypertext_. With anchorman you can markup terms,
create anchors, links, annotate abbreviations or just highlight specific
elements in text.

.. _hypertext: http://en.wikipedia.org/wiki/Hypertext

.. code::

    >>> import anchorman
    >>> text = "The quick brown fox jumps over the lazy dog."
    >>> links = [{'fox': {'value': '/wiki/fox'}},
                 {'dog': {'value': '/wiki/dog'}}]
    >>> a = anchorman.add(text, links)
    >>> a.result
    The quick brown <a href="/wiki/fox" class="anchorman">fox</a> jumps
    over the lazy <a href="/wiki/dog" class="anchorman">dog</a>.


Features
========

* global and item specific markups
* html/xml tags or highlighting
* handful of params to control replacements
* remove annotations by selector


Installation
============

To install Anchorman, simply:

.. code::

    pip install anchorman

Documentation
=============

For detailed usage examples read |docslink|.

.. |docslink| image:: https://readthedocs.org/projects/anchorman/badge/?version=latest
    :target: http://anchorman.readthedocs.org/en/latest/
    :alt: Documentation Status
