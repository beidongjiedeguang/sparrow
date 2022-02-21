from colour import Color
import numpy as np
from . import constant as _color_const


def color_to_rgb(color):
    if isinstance(color, str):
        return hex_to_rgb(color)
    elif isinstance(color, Color):
        return np.array(color.get_rgb())
    elif isinstance(color, (tuple, list, np.ndarray)):

        if isinstance(color[0], (int, np.int32, np.int64)):
            return np.array(color) / 255
        elif isinstance(color[0], (float, np.float32, np.float64)):
            return np.array(color)
        else:
            raise Exception(f"Invalid color type: {type(color[0])}")

    else:
        raise Exception(f"Invalid color type: {color}")


def color_to_rgba(color, alpha=1):
    return np.array([*color_to_rgb(color), alpha])


def rgb_to_color(rgb):
    try:
        return Color(rgb=rgb)
    except ValueError:
        return Color(_color_const.WHITE)


def rgba_to_color(rgba):
    return rgb_to_color(rgba[:3])


def rgb_to_hex(rgb):
    return "#" + "".join(
        hex(int_x // 16)[2] + hex(int_x % 16)[2]
        for x in rgb
        for int_x in [int(255 * x)]
    )


def hex_to_rgb(hex_code):
    hex_part = hex_code[1:]
    if len(hex_part) == 3:
        hex_part = "".join([2 * c for c in hex_part])
    return np.array([int(hex_part[i : i + 2], 16) / 255 for i in range(0, 6, 2)])


def invert_color(color):
    return rgb_to_color(1.0 - color_to_rgb(color))


def color_to_int_rgb(color):
    return (255 * color_to_rgb(color)).astype("uint8")


def color_to_int_rgba(color, opacity=1.0):
    alpha = int(255 * opacity)
    return np.array([*color_to_int_rgb(color), alpha])


def random_color():
    return Color(rgb=[np.random.random() for _ in range(3)])
