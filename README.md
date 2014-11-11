Anchorman
=========

Find words in HTML and replace them with a new element. Generally used as an
unsophisticated way of marking terms with anchors, e.g. `a` or `abbr` tags.

The low level function provided takes a string of HTML, a term to replace, a
function for creating the new element and a function for deciding if an element
should be updated. It returns an anchorman object with informations about the
replacements and the result text.

This function can be easily used to update a single occurrence or all occurrences
of a word but can also be used to build more complicated annotation strategies.

Linking example
---------------

    >>> import anchorman
    >>> links = [('fox', 'http://en.wikipedia.org/wiki/Fox'), ('dog', 'http://en.wikipedia.org/wiki/Dog')]
    >>> text = "<p>The quick brown fox jumps over the lazy dog.</p>"
    >>> anchorman.add_links(links, text)
    <p>The quick brown <a class="anchorman" href="http://www.wikipedia.en/fox">Fox</a> jumps over the lazy dog.</p>
 


Building
--------

    python setup.py develop

Installing
----------

    python setup.py install

Testing in a virtualenv
-----------------------

    virtualenv .
    ./bin/pip install -r requirements.txt
    ./bin/py.test test

Todos
-----

    * make it available for personalization of Element and attrib
    * use a customized class selector, default anchorman
    * add the counts for each linking ...may position too
