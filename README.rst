Welcome to Anchorman
====================

Turn your text into hypertext_. Annotate terms as html-tags or
just highlight them in text.

.. _hypertext: http://en.wikipedia.org/wiki/Hypertext


Features
--------

* mark elements as html/xml tags or add highlighting context
* specify replacement rules via settings
* consider text units (e.g. html-paragraphs) in replacement rules
* add your own element validator made easy


Usage examples
---------------

Basic example with simple cfg overwrite: Replace only one item in the whole text.
The first element of elements will satisfy this rule and end up as a link in the text.

.. code:: python

    >>> from anchorman.main import annotate
    >>> from anchorman.configuration import get_config
    >>> text = 'The quick brown fox jumps over the lazy dog.'
    >>> elements = [
            {'fox': {
                'value': '/wiki/fox', 'data-type': 'animal'}},
            {'dog': {
                'value': '/wiki/dog', 'data-type': 'animal'}}]
    >>> cfg = get_config()
    >>> cfg['setting']['replaces_at_all'] = 1
    >>> print annotate(text, elements, config=cfg)
    'The quick brown <a href="/wiki/fox" data-type="animal">fox</a> jumps over the lazy dog .'

See etc/link.yaml for options to configure the replacement process or the rules.


The item validator
++++++++++++++++++++

Inherit your own item validator. Item is the potential replacement.
Candidates is a list of processed and valide items ready to apply to text.
This unit bears valide items ready to apply to text in this intervall or unit.

.. code:: python

    >>> from anchorman.generator.candidate import data_val
    >>> def validator(item, candidates, this_unit, setting):
    ...    values = data_val(item, None)
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
    >>> cfg = get_config()
    >>> unit = {'key': 't', 'name': 'text'}
    >>> cfg['setting']['text_unit'].update(unit)
    >>> cfg['markup'] = {'tag': {'tag': 'div'}}
    >>> annotated = annotate(s_text, s1_elements, config=cfg)
    >>> annotated2 = annotate(annotated, s11_elements, config=cfg)
    >>> cfg3 = cfg.copy()
    >>> cfg3['markup'] = {'tag': {'tag': 'span'}}
    >>> annotated3 = annotate(annotated2, s2_elements, config=cfg3)

The text annotated3 looks like this:

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
* more schema.org examples
* implement an original text/key replacement logic (kicked value, value_key)
* check context of replacement: do not add links in links, or inline of overlapping elements, ...
* replace only one item of an entity > e.g. A. Merkel, Mum Merkel, ...
* implement a replacement logic for coreference chains
