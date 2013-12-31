# -*- coding: utf-8 -*-

"""
gmncurses.ui.widgets.utils
~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from x256 import x256


def color_to_hex(color):
    """
    Given either an hexadecimal or HTML color name, return a the hex
    approximation without the `#`.
    """
    if color.startswith("#"):
        return x256.from_hex(color.strip("#"))
    else:
        return x256.from_html_name(color)
