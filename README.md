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

    from anchorman.linkit import add_in_text_links
    tags = [("Tarn", "http://tarnbarford.net")]
    html = "<p>Hey, Tarn!</p>"
    add_in_text_links(html, tags)

    > u'<p>Hey, <a class="anchorman" href="http://tarnbarford.net">Tarn</a>!</p>'

## Custom example

    from anchorman.linkit import replace_token
    from lxml import etree
    from functools import partial

    def create_abbr(match):
        """
        Create an lxml `abbr` element. The `term` parameter is the search term,
        the `value` is used to pass what to do with the term and the match is 
        the string that was found.
        """
        element = etree.Element('abbr')
        element.attrib["title"] = "Tarn Barnford"
        element.text = match
        return element


    def is_abbr(element):
        """
        Return true if the element is an `abbr` tag so we don't add `abbr` inside
        `abbr` tags. 
        """
        return element is not None and element.tag == "abbr"

    html = "<p>Hey, Tarn!</p>"

    replace_token(html, "tarn", create_abbr, is_abbr)

    > (u'<p>Hey, <abbr title="Tarn Barnford">TB</abbr>!</p>', True) 


## Building  

    python setup.py develop

## Installing 

    python setup.py install

## Testing in a virtualenv

    virtualenv .
    ./bin/pip install -r requirements.txt
    ./bin/py.test test
