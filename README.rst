## Anchorman

Find words in HTML and replace them with a new element. Generally used as an
unsophisticated way of marking terms with anchors, e.g. `a` or `abbr` tags.

Provides functions to abstract the searching for and replacing of a term or 
multiple terms in a string of HTML. 

The low level function provided takes a string of HTML, a term to replace, a
function for creating the new element and a function for deciding if an element
should be updated. It returns a new string and a Boolean to indicate if an
update was made.

This function can be easily used to update a single occurrence or all occurrences
of a word but can also be used to build more complicated annotation strategies.

## Linking example

    text = '<p>The quick brown fox jumps over the lazy dog.</p><p>Foxes are small-to-medium-sized, omnivorous mammals belonging to several genera of the Canidae family.</p>'
    links = [('fox', 'http://en.wikipedia.org/wiki/Fox'), ('mammals', 'http://en.wikipedia.org/wiki/Mammal')]
    # print replace_token(text, "Fox.", "hello", link_fn)
    print add_links(text, links)


    >>> import anchorman
    >>> html = "<p>The quick brown fox jumps over the lazy dog.</p>"
    >>> links = [('fox', 'http://en.wikipedia.org/wiki/Fox')]
    >>> anchorman.add_links(html, links)

    <p>The quick brown <a class="anchorman" href="http://en.wikipedia.org/wiki/Fox">fox</a>


## Building  

    python setup.py develop

## Installing 

    python setup.py install

## Testing in a virtualenv

    virtualenv .
    ./bin/pip install -r requirements.txt
    ./bin/py.test test
