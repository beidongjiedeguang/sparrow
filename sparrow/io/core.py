from collections import Counter
from functools import wraps
import pickle
import numpy as np


def save_var(filename, data):
    with open(filename, "wb") as fw:
        pickle.dump(data, fw)


def load_var(filename):
    with open(filename, "rb") as fi:
        data = pickle.load(fi)
    return data


def broadcast(func):  # It can be replaced by `np.vectorize`
    """Only for a functions with a single argument
    example:
    @broadcast
    def f(x):
        # A function that can map only a single element
        if x==1 or x==0:
            return x
        else:
            return f(x-1)+f(x-2)

    >> f([2,4,10])
    >> (1, 3, 832040)
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        value_list = []
        for arg in args:
            value_list.append(func(arg, **kwargs))
        return tuple(value_list)

    return wrapper
