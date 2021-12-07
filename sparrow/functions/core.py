from functools import reduce
import inspect
import numpy as np
import operator as op


def clamp(x, x_min, x_max):
    """ Clamp a number to same range.
    Examples:
        >>> clamp(-1, 0, 1)
        >>> 0
        >>> clamp([-1, 2, 3], [0, 0, 0], [1, 1, 1])
        >>> [0, 1, 1]
    """
    return np.maximum(x_min, np.minimum(x_max, x))


CHOOSE_CACHE = {}


def choose_using_cache(n, r):
    if n not in CHOOSE_CACHE:
        CHOOSE_CACHE[n] = {}
    if r not in CHOOSE_CACHE[n]:
        CHOOSE_CACHE[n][r] = choose(n, r, use_cache=False)
    return CHOOSE_CACHE[n][r]


def choose(n, r, use_cache=True):
    if use_cache:
        return choose_using_cache(n, r)
    if n < r:
        return 0
    if r == 0:
        return 1
    denom = reduce(op.mul, range(1, r + 1), 1)
    numer = reduce(op.mul, range(n, n - r, -1), 1)
    return numer // denom


def get_num_args(function):
    return len(get_parameters(function))


def get_parameters(function):
    return inspect.signature(function).parameters
