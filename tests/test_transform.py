import numpy as np
from einops import rearrange, reduce, asnumpy, parse_shape, repeat


def test_array():
    c = 3
    w = 100
    h = 50
    a = np.arange(c * w * h, dtype='float').reshape((c, w, h))
    assert a.shape == (c, w, h)
    assert rearrange(a, 'c w h -> w h c').shape == (w, h, c)

    a = reduce(a, 'c w h -> w h', 'mean')
    assert a.shape == (w, h)
    assert repeat(a, 'w h -> w h c', c=3).shape == (w, h, 3)
