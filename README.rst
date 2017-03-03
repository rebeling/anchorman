# Welcome to Anchorman

.. image:: https://img.shields.io/pypi/v/anchorman.svg
   :target: https://pypi.python.org/pypi/anchorman
   :alt: Latest Version

.. image:: https://travis-ci.org/rebeling/anchorman.svg?branch=master
   :target: https://travis-ci.org/rebeling/anchorman

Turn your text into [hypertext](http://en.wikipedia.org/wiki/Hypertext) 
and enrich the content. Anchorman finds terms in text and replaces
them with another representation.

The replacement is rule-based. Each term is checked against the rules
and will be applied if valid.

    # How many items will be marked at all in the text.
    replaces_at_all: 5

    # Input term has to be exact match in text.
    case_sensitive: true


## Features

* replacement rules
* consider text units in the rules (e.g. paragraphs)
* replace only n items of the same item
* specify restricted_areas for linking by tag: a, img
* sort elements by value before apply them
* return applied elements


## Usage

    >>> from anchorman import annotate
    >>> text = 'The quick brown fox jumps over the lazy dog.'
    >>> elements = [{'fox': {'value': '/wiki/fox', 'data-type': 'animal'}}]
    >>> print annotate(text, elements)
    'The quick brown <a href="/wiki/fox" data-type="animal">fox</a> jumps over the lazy dog.'


## Installation

To install Anchorman, simply:

    pip install anchorman


## Credits and contributions

We published this at github and pypi to provide our solution to you.
Pleased for feedback and contributions.

Thanks [@tarnacious](https://github.com/tarnacious) for inspiration
and first steps.


## Todo

* check if position exist in input and save extra processing
* html.parser vs lxml in bs4 - benchmarks and drawbacks

<img src="https://raw.githubusercontent.com/rebeling/anchorman/master/docs/anchorman.png" width="200">

Stay tuned.
