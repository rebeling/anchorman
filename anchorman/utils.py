import time
import sys
import inspect
from time import strftime


def timeit(method):
    def timed(*args, **kw):

        bench = []
        for r in xrange(10):
            ts = time.time()
            result = method(*args, **kw)
            te = time.time()
            bench.append(te-ts)
            # print '%r (%r, %r) %2.4f sec' % \
            #       (method.__name__, args, kw, te-ts)
            # print '%r \t\t%2.4f sec' % (method.__name__, te-ts)
        print '%r \t\t%2.4f sec' % (method.__name__, sum(bench)/len(bench))
        return result
    return timed


def filter_applied_against_input(elements, to_be_applied):
    """Return a tuple of applied items and the rest."""
    applied = [token for _, _, token, _ in to_be_applied]
    rest = [x for x in elements if x.keys()[0] not in applied]
    return applied, rest


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
