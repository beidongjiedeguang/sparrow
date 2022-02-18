from functools import reduce
import inspect
import numpy as np
import scipy.stats as st
import operator as op


def gaussian(x, sigma, miu):
    """Standard Gaussian function"""
    a = 1 / np.sqrt(2 * np.pi * sigma**2)
    return a * np.exp(-((x - miu) ** 2) / (2 * sigma**2))


def norm_gaussian(x, sigma, miu):
    """Normalized Gaussion fuction"""
    return np.exp(-((x - miu) ** 2) / (2 * sigma**2))


def gaussian_2d(U, V, sigma, miu):
    a = 1 / np.sqrt(2 * np.pi * sigma**2)
    res_max = a * np.exp(
        -((0 - miu) ** 2 + (0 - miu) ** 2) / (2 * sigma**2)
    )  # For normalization
    res = a * np.exp(-((U - miu) ** 2 + (V - miu) ** 2) / (2 * sigma**2))
    return res / res_max  # Normalized


def cdf(x, sigma, miu):
    return st.norm.cdf(x, loc=miu, scale=sigma)


def gaussion_kernel(kernlen=3, nsig=3):
    x = np.linspace(-nsig, nsig, kernlen + 1)
    kern1d = np.diff(st.norm.cdf(x))
    kern2d = np.outer(kern1d, kern1d)
    return kern2d / kern2d.sum()


if __name__ == "__main__":
    x = np.repeat(np.arange(5).reshape(1, -1), repeats=5, axis=0)
    y = np.repeat(np.arange(5).reshape(-1, 1), repeats=5, axis=1)

    # print(x)
    # print(y)
    print(gaussian_2d(x, y, sigma=3, miu=2))
    print(gaussion_kernel(5, 3))
