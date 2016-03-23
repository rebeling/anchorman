# -*- coding: utf-8 -*-
import sys
import inspect
from time import strftime


def log(msg):
    """Project logger.

    :param msg: Error message string.
    """
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    sys.stdout.write('[%s] log: %s %s' % (
        strftime("%Y-%m-%d %H:%M:%S"), mod.__name__, msg
        )
    )
