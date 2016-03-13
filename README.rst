Welcome to Anchorman
---------------------

Turn your text into hypertext_ and enrich the content. Anchorman takes a list
of terms and a text. It finds the terms in your text and replaces them with an
html-element representation.

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

    >>> from anchorman.generator.candidate import data_values
    >>> def validator(item, candidates, this_unit, setting):
    ...    values = data_values(item)
    ...    if values['score'] == 42.0 and values['type'] == 'city':
    ...        return True
    ...    else:
    ...        return False
    ...
    >>> print annotate(text, elements, own_validator=[validator])


Apply schema.org
++++++++++++++++++

Not so handy approach is to create contexts with multiple annotation calls.
But the logic to annotate data around and in each other is pretty hacky as
the following example shows:


.. code:: python

    >>> s_text = 'Angela Merkel, CDU, Bundeskanzlerin'
    >>> s1_elements = [
    ...     {"Angela Merkel, CDU, Bundeskanzlerin": {
    ...         'itemtype': 'http://schema.org/Person',
    ...         'itemscope': None}}
    ...     ]
    ...
    >>> s11_elements = [
    ...     {"CDU": {
    ...         'itemtype': 'http://schema.org/Organization',
    ...         'itemscope': None}}
    ...     ]
    ...
    >>> s2_elements = [
    ...     {"Angela Merkel": {
    ...         'itemprop': 'name'}},
    ...     {"CDU": {
    ...         'itemprop': 'name'}},
    ...     {"Bundeskanzlerin": {
    ...         'itemprop': 'jobtitle'}}
    ...     ]
    ...
    >>> from anchorman import get_config
    >>> cfg = get_config()
    >>> unit = {'key': 't', 'name': 'text'}
    >>> cfg['setting']['text_unit'].update(unit)
    >>> cfg['markup'] = {'tag': {'tag': 'div'}}
    >>> annotated = annotate(s_text, s1_elements, config=cfg)
    >>> annotated2 = annotate(annotated, s11_elements, config=cfg)
    >>> cfg3 = cfg.copy()
    >>> cfg3['markup'] = {'tag': {'tag': 'span'}}
    >>> annotated3 = annotate(annotated2, s2_elements, config=cfg3)


Then text annotated3 looks like this:

.. code:: html

    <div itemscope itemtype="http://schema.org/Person">
        <span itemprop="name">Angela Merkel</span>,
        <div itemscope itemtype="http://schema.org/Organization">
            <span itemprop="name">CDU</span>
        </div>,
        <span itemprop="jobtitle">Bundeskanzlerin</span>
    </div>


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
* add sentence splitter or add to readme example with <s></s>
* check if position exist in input and save extra processing
* check context of replacement: do not add links in links, or inline of overlapping elements
* replace only one item of an entity > e.g. A. Merkel, Mum Merkel, ...
* implement a replacement logic for coreference chains
* add more schema.org examples
