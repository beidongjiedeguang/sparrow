import numpy as np


def get_continue_subseries(series, idx):
    """
    Examples:
        >>> series = [0, 2, 3, 4, 5, 7, 8, 10, 11]
        >>> get_continue_subseries(series, 2)
        array([2, 3, 4, 5])
        >>> get_continue_subseries(series, -1)
        array([10, 11])
        >>> get_continue_subseries(series, 0)
        array([0])
    """

    idx_min, ref_min = idx, series[idx]
    while ref_min == series[idx_min]:
        idx_min -= 1
        ref_min -= 1

    idx_max, ref_max = idx, series[idx]
    while idx_max < len(series) and ref_max == series[idx_max]:
        idx_max += 1
        ref_max += 1
    idxs = np.arange(idx_min + 1, idx_max)
    return np.asarray(series)[idxs]


def series_concatenate_and_sort(series_a, series_b):
    """
    :returns:
        concatenated and sorted series.
        series_b's index in concatenated series.
    """
    t_series = np.concatenate((series_a, series_b))
    sorted_idxs = np.argsort(t_series)
    series_b_idxs = np.argsort(sorted_idxs)[-len(series_b) :]
    return t_series[sorted_idxs], series_b_idxs


def calc_continue_series_dict(target_series, key_series):
    """
    Examples:
        >>> a = (0, 1, 4, 5, 7, 8, 9, 11, 12, 13, 15, 16, 17)
        >>> b = (2, 10,)
        >>> calc_continue_series_dict(a, b)
        {2: array([0, 1, 2]), 10: array([ 7,  8,  9, 10, 11, 12, 13])}
    """
    concatenated_series, flag_idxs = series_concatenate_and_sort(
        target_series, key_series
    )
    target_dict = {}
    for idx in range(len(key_series)):
        subseries = get_continue_subseries(concatenated_series, flag_idxs[idx])
        target_dict.setdefault(key_series[idx], subseries)
    return target_dict


if __name__ == "__main__":
    a = (0, 1, 4, 5, 7, 8, 9, 11, 12, 13, 15, 16, 17)
    b = (2, 10, 14)
    print(calc_continue_series_dict(a, b))
    # import doctest
    # doctest.testmod()
