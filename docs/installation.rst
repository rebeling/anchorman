


Installation
============

Install anchorman via pip, master branch status: |travis|

.. code::

    pip install anchorman

or from source code

.. code::

    git clone https://github.com/rebeling/anchorman.git && cd anchorman
    python setup.py install

test it in a virtual environment

.. code::

    virtualenv .
    ./bin/pip install -r requirements.txt
    ./bin/py.test test

or locally

    py.test --cov=anchorman --cov-report term-missing -v -s

.. |travis| image:: https://travis-ci.org/rebeling/anchorman.svg?branch=master
    :target: https://travis-ci.org/rebeling/anchorman
    :alt: Built Status



