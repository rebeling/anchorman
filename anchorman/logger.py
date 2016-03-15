# -*- coding: utf-8 -*-
import sys
import inspect


def log(msg):
    """Create a flexible logger."""
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    sys.stdout.write('[time] log: %s %s' % (mod.__name__, msg))
