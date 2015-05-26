
Performance
===========

1000 items were processed with mean text len of 1800 characters. Same
list of links was applied and around 11 times per text items augemented.

.. code::

    # without markup
    min  0.00060 s
    max  0.00891 s
    mean 0.00152 s

    # with basic markup
    min  0.00061 s
    max  0.00929 s
    mean 0.00158 s

    # highlighting
    min  0.00057 s
    max  0.00783 s
    mean 0.00117 s

It is pretty fast already, but we need to check with larger link list and
also some other cases > this was add links only, what about remove, apply
other markup in between etc.

