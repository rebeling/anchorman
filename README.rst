Welcome to Anchorman
====================

Turn your text into hypertext_. With anchorman you can markup terms,
create anchors, links, annotate abbreviations or just highlight specific
elements in text.

.. _hypertext: http://en.wikipedia.org/wiki/Hypertext


Features
--------

* mark elements as html/xml tags or highlight context
* specify replacement rules via setting overwrite
* consider text units (e.g. html-paragraphs) in replacement rules
* add your own element validator made easy


Usage
----------

Basic example with config overwrite.

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

See etc/link.yaml for options to configure the replacement process or rules.


Inherit your own item validator. Item is the potential replacement. Candidates
is a list of processed, valide and items ready to be applied to text. And this
unit bears processed, valide and items ready to be applied to text in this
intervall and finally the setting dict from config.


.. code:: python

    >>> def validator(item, candidates, this_unit, setting):
    ...    values = data_val(item, None)
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

We published this at github and pypi to provide our solution to others, to get feedback and find contributers in the open source.

Thanks `Tarn Barford`__ for inspiration and first steps.

.. _TheAustralien: https://tarnbarford.net/
__ TheAustralien_


Todo
---------
* check context of replacement: do not add links in links, or inline of overlapping elements, ...
* replace only one item of an entity > e.g. A. Merkel, Mum Merkel, ...
