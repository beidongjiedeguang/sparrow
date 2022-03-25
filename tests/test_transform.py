import numpy as np
from einops import rearrange, reduce, asnumpy, parse_shape
from sparrow.transform import repeat


def test_array():
    c, w, h = 3, 100, 50
    a = np.arange(c * w * h, dtype="float").reshape((c, w, h))
    assert a.shape == (c, w, h)
    assert rearrange(a, "c w h -> w h c").shape == (w, h, c)

    a = reduce(a, "c w h -> w h", "mean")
    assert a.shape == (w, h)


def test_repeat():
    a1 = np.random.randn(10)
    assert repeat(a1, 3, 0).shape == (3, 10)
    assert repeat(a1, 3, -1).shape == (10, 3)

    a2 = np.random.randn(20, 30)
    assert repeat(a2, 3, 0).shape == (3, 20, 30)
    assert repeat(a2, 3, -1).shape == (20, 30, 3)

    a3 = np.random.randn(20, 30, 3)
    assert repeat(a3, 10, 0).shape == (10, 20, 30, 3)
    assert repeat(a3, 10, -1).shape == (20, 30, 3, 10)
    assert repeat(a3, 10, 1).shape == (
        20,
        10,
        30,
        3,
    )
