.. Anchorman documentation master file, created by
   sphinx-quickstart on Mon May 18 12:53:24 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Welcome to Anchorman
========================

Anchorman turns your text into hypertext_. With anchorman you can markup
terms, create anchors, links, annotate abbreviations or just highlight
specific elements in text.

.. _hypertext: http://en.wikipedia.org/wiki/Hypertext

.. code::

    >>> import anchorman
    >>> text = "The quick brown fox jumps over the lazy dog."
    >>> links = [{'fox': {'value': '/wiki/fox'}},
                 {'dog': {'value': '/wiki/dog'}}]
    >>> a = anchorman.add(text, links)
    >>> print a
    The quick brown <a href="/wiki/fox" class="anchorman">fox</a> jumps
    over the lazy <a href="/wiki/dog" class="anchorman">dog</a>.

Check the user guide for detailed introduction and more examples of
all the implemented features.


User Guide
-----------

This part of the documentation, provides step-by-step
instructions for getting the most out of Anchorman.

.. toctree::
   :maxdepth: 2

   firststeps
   installation
   performance


.. Code
.. -----------

.. If you are looking for information on a specific function,
.. class or method, this part of the documentation is for you.

.. .. toctree::
..    :maxdepth: 2

..    api


Credits
-----------

`Tarn Barford`__ is the father of this - he had the idea and crafted
the first implementation - and I_ took over mothers part ...grow, feed,
clean up, etc.

We published this at github and pypi to provide our solution to others,
to get feedback and find contributers in the open source.

.. _Python: https://tarnbarford.net/
__ Python_

.. _I: http://rebeling.net/


Indices and tables
----------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
