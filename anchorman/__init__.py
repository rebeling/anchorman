#!/usr/bin/env python
# encoding: utf-8

from .linkit import remove_links, add_links
from .anchorman import *


"""
anchorman library
~~~~~~~~~~~~~~~~~~~~~
Anchorman is a library, written in Python.

   >>> import anchorman
   >>> links = [('Fox', 'http://www.wikipedia.en/fox')]
   >>> text = "<p>The quick brown fox jumps over the lazy dog.</p>"
   >>> anchorman.add(text, links)
   <p>The quick brown <a class="anchorman" href="http://www.wikipedia.en/fox">Fox</a> jumps over the lazy dog.</p>


:copyright: (c) 2015 by Tarn Barford.
:license: Apache 2.0, see LICENSE for more details.
"""

__title__ = 'anchorman'
__version__ = '0.0.1'
__author__ = 'Tarn Barford'
__author_email__ = 'tarn@tarnbarford.net'
__url__ = 'https://github.com/tarnacious/anchorman'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2015 Tarn Barford'
