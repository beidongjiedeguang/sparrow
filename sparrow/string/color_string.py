from ..color import color_to_int_rgb, color_const

CSI = "\033["
OSC = "\033]"
OFF = CSI + "0m"


def __set_rgb(RGB_fore=(240, 85, 85), SRG=0, RGB_back=None):
    """Get foreground or background color chars
    see https://my.oschina.net/dingdayu/blog/1537064
    inputs:
        RGB_fore: rgb list or tupe of foreground, e.g. [255, 0, 0]
        SRG:  the style of font
        SRG options: see https://en.wikipedia.org/wiki/ANSI_escape_code#SGR
            | 0  |     Close all formats and revert to the original state
            | 1  |     Bold (increased intensity)
            | 2  |     Faint (decreased intensity)
            | 3  |     Italics
            | 4  |     Underline (single line)
            | 5  |     Slow Blink
            | 6  |     Rapid Blink
            | 7  |     Swap the background color with the foreground color
    """
    fore_color = f"{CSI}{SRG};38;2;{RGB_fore[0]};{RGB_fore[1]};{RGB_fore[2]}m"
    if RGB_back is None:
        back_color = ""
    else:
        back_color = f"{CSI}{SRG};48;2;{RGB_back[0]};{RGB_back[1]};{RGB_back[2]}m"
    return fore_color + back_color


def _rgb_str(string, RGB_fore=(240, 85, 85), SRG=0, RGB_back=None):
    return __set_rgb(RGB_fore, SRG, RGB_back) + string + OFF


def rgb_string(string, color=color_const.RED, **kwargs):
    """Return the string with color.
    :param string: The string will be colored.
    :param color: can be rgb list [255, 255, 255]  or hex string "#ffffff".
    :param `SRG`, `RGB_back` see function `__set_grb()`
    :return Colored string.
    """
    rgb = color_to_int_rgb(color)
    return _rgb_str(string, rgb, **kwargs)
