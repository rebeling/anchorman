Welcome to Anchorman
---------------------

Turn your text into hypertext_ and enrich the content. Anchorman takes a
list of terms and a text. It finds the terms in this text and replaces
them with another representation.

The replacement is guided by rules like the following. Each term is checked
against the rules and will be applied if valid.

.. code:: yaml

    # How many items will be marked at all in the text.
    replaces_at_all: 5

    # Input term has to be exact match in text.
    case_sensitive: true

The text is analysed via intervalltree and the replacement happens on position
and context.


.. _hypertext: http://en.wikipedia.org/wiki/Hypertext


Features
--------

* replacement rules via settings
* consider text units in the rules (e.g. paragraphs)
* add your own element validator made easy
* replace only n items of the same item
* specify restricted_areas for linking by tag: a, img as default
* return applied elements
* sort elements by value before apply to text


Usage
------

The first element of elements is find in text and replaced with a link tag.

.. code:: python

    >>> from anchorman import annotate
    >>> text = 'The quick brown fox jumps over the lazy dog.'
    >>> elements = [{'fox': {'value': '/wiki/fox', 'data-type': 'animal'}}]
    >>> print annotate(text, elements)
    'The quick brown <a href="/wiki/fox" data-type="animal">fox</a> jumps over the lazy dog .'

See etc/link.yaml for options to configure the replacement process and rules.


The item validator
++++++++++++++++++++

Inherit your own item validator. Item is the potential replacement.
Candidates is a list of processed and valid items ready to apply to text.
This unit bears valid items ready to apply to text in this intervall or unit.

.. code:: python

    >>> from anchorman.generator.candidate import get_data_of
    >>> def validator(item, candidates, this_unit, setting):
    ...    values = get_data_of(item)
    ...    if values['score'] == 42.0 and values['type'] == 'city':
    ...        return True
    ...    else:
    ...        return False
    ...
    >>> print annotate(text, elements, own_validator=[validator])


Installation
------------

To install Anchorman, simply:

.. code::

    pip install anchorman


Credits and contributions
--------------------------

We published this at github and pypi to provide our solution to you.
Pleased for feedback and contributions.

Thanks `Tarn Barford`__ for inspiration and first steps.

.. _TheAustralien: https://tarnbarford.net/
__ TheAustralien_


Todo
---------
* write tests for the settings and rules like examples or how to

* check if position exist in input and save extra processing
* validate text und elements
* html.parser vs lxml in bs4 - think about config
* ValueError: IntervalTree: Null Interval objects
* add sentence splitter or add to readme example with <s></s>
* replace only one item of an entity > e.g. A. Merkel, Mum Merkel, ...
* implement a replacement logic for coreference chains


Feedback and thanks for reading.
