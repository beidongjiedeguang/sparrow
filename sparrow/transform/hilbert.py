import numpy as np


def get_hilbert_1d_array(image: np.ndarray):
    from hilbert import decode, encode  # $ pip install numpy-hilbert-curve
    num_dims = 2
    num_bits = np.log2(image.shape[0] * image.shape[1]) / num_dims
    num_bits = int(num_bits)
    max_hil = 2 ** (num_bits * num_dims)
    hilberts = np.arange(max_hil)
    locs = decode(hilberts, num_dims, num_bits)

    image1d = []
    for coord in locs:
        image1d.append(image[coord[0], coord[1]])
    return np.array(image1d)[None, ...]
