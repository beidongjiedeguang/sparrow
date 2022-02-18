import numpy as np
import Levenshtein  # pip install python-Levenshtein

"""
Some common distance function
"""


def euclidean_dist(vec1, vec2):
    assert vec1.shape == vec2.shape
    return np.sqrt(np.sum((vec1 - vec2) ** 2))


def manhattan_dist(vec1, vec2):
    return np.sum(np.abs(vec1 - vec2))


def chebyshev_dist(vec1, vec2):
    return np.max(np.abs(vec1 - vec2))


def minkowski_dist(vec1, vec2, p=2):
    """
    :param: `p` The meaning of norm.
        p=1: dist = manhattan_dist
        p=2: dist = euclidean_dist
        p=inf: dist = chebyshev_dist
    """
    s = np.sum(np.power(vec2 - vec1, p))
    return np.power(s, 1 / p)


def cosine_dist(vec1, vec2, p=2):
    # np.linalg.norm(vec, ord=1) 计算p=1范数,默认p=2
    return (vec1.T @ vec2) / (np.linalg.norm(vec1, ord=p) * np.linalg.norm(vec2, ord=p))


def distance(a, b):
    return Levenshtein.ratio(a, b)


def hamming(x, y):
    return np.sum(x != y) / len(x)


def jaccard():
    pass
