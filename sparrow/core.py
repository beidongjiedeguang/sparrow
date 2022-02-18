from collections import Counter
from functools import wraps
import pickle
import numpy as np
from deprecated import deprecated


@deprecated(version="0.5.0", reason="Deprecated, use `sparrow.io.core` instead.")
def save_var(filename, data):
    with open(filename, "wb") as fw:
        pickle.dump(data, fw)


@deprecated(version="0.5.0", reason="Deprecated, use `sparrow.io.core` instead.")
def load_var(filename):
    with open(filename, "rb") as fi:
        data = pickle.load(fi)
    return data


def clamp(x, x_min, x_max):
    """Clamp a number to same range.
    It's equivalent to np.clip()
    Examples:
        >>> clamp(-1, 0, 1)
        >>> 0
        >>> clamp([-1, 2, 3], [0, 0, 0], [1, 1, 1])
        >>> [0, 1, 1]
    """
    return np.maximum(x_min, np.minimum(x_max, x))


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


class _Dict_enhance(dict):
    """Enables the dictionary to be dot operated"""

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self


def dict_dotable(dic):
    """
    : input: a dictionary
    : output: an enhanced dictionary
    Example:
        enhance_dic = dict_dotable(dic)
    then, you can operate an enhanced dictionary like this:
        enhance_dic.key1.key2. ...
    """
    dic = _Dict_enhance(dic)
    for i in dic:
        if type(dic[i]) == dict:
            dic[i] = dict_dotable(dic[i])
    return dic


class Constant:
    """
    define a constant like C language.
    `object.__setattr__(self, name, value)`
    this built-in function will called when assigning values to properties of the class

    `object.__dict__` holds all writable attributes in object,
    key as variable name and value as variable value.
    """

    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise ValueError("Constant value can't be changed")
        else:
            self.__dict__[name] = value


def number_digits(number):
    res = number
    digit = 1
    if res >= 1:
        while res > 10:
            digit += 1
            # res, mod = np.divmod(res, 10)
            res //= 10
    else:
        while res < 1:
            digit -= 1
            res *= 10
    return digit


def num_digits(number_like):
    number_str = str(int(str(number_like)))
    return len(number_str)


def sort_count(_list: list):
    """
    返回lis的由大到小排序好的元素列表
    Example:
    l = np.array([2,2,2,2,5,5,3,9,9])
    sort_count(l) : [(2, 4), (5, 2), (9, 2), (3, 1)]
    # return [2, 5, 9,3], [4, 2, 2, 1]
    """
    a = Counter(_list)
    b = sorted(a.items(), key=lambda item: item[1], reverse=True)
    # idx, counts = [b[i][0] for i in range(len(b))], [b[i][1] for i in range(len(b))]
    return b


def reduce_list_element(array, *elems):
    """
    example:
    a = [ 5, 6, 6, 7, 8, 9, 9]
    reduce_list_element(a, 6, 9)
    print(a)
    >> [ 5, 7, 8]
    """
    length = len(array)
    for idx in range(length):
        index = length - idx - 1
        for elem in elems:
            if array[index] == elem:
                array.pop(index)
