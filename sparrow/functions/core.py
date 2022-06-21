from functools import partial, wraps, reduce
import inspect
import numpy as np
import operator as op
import random
import time
import pandas as pd
from .utils import exists

__all__ = ["topk", "dict_topk", "random_idx", "clamp", "get_num_args", "get_parameters"]


def dict_topk(a: dict, k: int, reverse=False) -> pd.DataFrame:
    df = pd.DataFrame({'key': a.keys(), 'value': a.values()})
    if not reverse:
        return df.nlargest(k, 'value')
    else:
        return df.nsmallest(k, 'value')


def topk(a, k, axis=-1, largest=True, sort=True):
    """Series top K"""
    a = np.asanyarray(a)
    if axis is None:
        axis_size = a.size
    else:
        axis_size = a.shape[axis]
    assert 1 <= k <= axis_size

    if largest:
        index_array = np.argpartition(a, axis_size - k, axis=axis)
        topk_indices = np.take(index_array, -np.arange(k) - 1, axis=axis)
    else:
        index_array = np.argpartition(a, k - 1, axis=axis)
        topk_indices = np.take(index_array, np.arange(k), axis=axis)
    topk_values = np.take_along_axis(a, topk_indices, axis=axis)
    if sort:
        sorted_indices_in_topk = np.argsort(topk_values, axis=axis)
        if largest:
            sorted_indices_in_topk = np.flip(sorted_indices_in_topk, axis=axis)
        sorted_topk_values = np.take_along_axis(
            topk_values, sorted_indices_in_topk, axis=axis
        )
        sorted_topk_indices = np.take_along_axis(
            topk_indices, sorted_indices_in_topk, axis=axis
        )
        return sorted_topk_values, sorted_topk_indices
    return topk_values, topk_indices


def random_idx(idx_range, exclude_idx=None):
    random.seed(time.time())
    rand_idx = random.randint(*idx_range)
    if rand_idx == exclude_idx:
        return random_idx(idx_range, exclude_idx)
    else:
        return rand_idx


def clamp(x, x_min=None, x_max=None):
    """Clamp a number to same range.
    Examples:
        >>> clamp(-1, 0, 1)
        >>> 0
        >>> clamp([-1, 2, 3], [0, 0, 0], [1, 1, 1])
        >>> [0, 1, 1]
    """
    assert exists(x_min) or exists(x_max)
    if exists(x_min):
        x = np.maximum(x, x_min)
    if exists(x_max):
        x = np.minimum(x, x_max)
    return x


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
