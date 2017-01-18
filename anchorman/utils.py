import time
import sys
import inspect
from time import strftime
import logging
logger = logging.getLogger('anchorman')


def timeit(method):
    def timed(*args, **kw):
        bench = []
        for r in xrange(10):
            ts = time.time()
            result = method(*args, **kw)
            te = time.time()
            bench.append(te-ts)
        print '%r \t\t%2.4f sec' % (method.__name__, sum(bench)/len(bench))
        return result
    return timed


def filter_applied_against_input(elements, to_be_applied):
    """Return a tuple of applied items and the rest."""
    # applied = [token for _, _, token, _ in to_be_applied]
    def elem(token):
        for x in elements:
            if token == x.keys()[0]:
                return x

    applied = [elem(token) for _, _, token, _ in to_be_applied]
    rest = [x for x in elements if x not in applied]
    log("\nApplied:\n  {}".format('\n  '.join([str(a) for a in applied])))
    log("\nRest:\n  {}".format('\n  '.join([str(a) for a in rest])))
    return applied, rest


def log(msg, level=None, logger=logger):
    """Project logger.

    :param msg: Error message string.
    """
    # print logging._levelNames[logger.level] == 'INFO'
    # if logger.isEnabledFor(logging.DEBUG):

    if level == 'INFO':
        logger.info(msg)
    else:
        logger.debug(msg)


def set_and_log_level(log_level, logger=logger):
    """Log the global level via INFO at start."""
    logger.setLevel(logging.getLevelName('INFO'))
    log('log_level {}'.format(log_level), level='INFO')
    logger.setLevel(logging.getLevelName(log_level))
