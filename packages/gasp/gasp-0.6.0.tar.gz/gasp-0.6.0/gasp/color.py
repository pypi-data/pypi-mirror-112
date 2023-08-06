#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This program is part of GASP, a toolkit for newbie Python Programmers.
# Copyright 2020 (C) Richard Crook, Gareth McCaughan, and the GASP Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# GASP color module
# Developed by Richard Martinez

"""Publicly accessible API of GASP.

GASP color is automatically imported when using `from gasp import *`.
To import GASP color using `from gasp import games`, also include `from gasp import color`.

To use any methods in this application, you must preface it with '`color.`'.
"""

ALICEBLUE = "#F0F8FF"
ANTIQUEWHITE = "#FAEBD7"
AQUA = "#00FFFF"
AZURE = "#F0FFD4"
BEIGE = "#F5F5DC"
BISQUE = "#FFE4C4"
BLACK = "#000000"
BLANCHEDALMOND = "#FFFFCD"
BLUE = "#0000FF"
BLUEVIOLET = "#8A2BE2"
BROWN = "#A52A2A"
BURLYWOOD = "#DEB887"
CADETBLUE = "#5F9EA0"
CHARTREUSE = "#7FFF00"
CHOCOLATE = "#D2691E"
CORAL = "#FF7F50"
CORNFLOWERBLUE = "#6495ED"
CORNSILK = "#FFF8DC"
CRIMSON = "#DC143C"
CYAN = "#00FFFF"
DARKBLUE = "#00008B"
DARKCYAN = "#008B8B"
DARKGOLDENROD = "#B8860B"
DARKGRAY = "#A9A9A9"
DARKGREEN = "#006400"
DARKKHAKI = "#BDB76B"
DARKMAGENTA = "#8B008B"
DARKOLIVEGREEN = "#556B2F"
DARKORANGE = "#FF8C00"
DARKORCHID = "#9B32CC"
DARKRED = "#8B0000"
DARKSALMON = "#E9967A"
DARKSEAGREEN = "#8FBC8F"
DARKSLATEBLUE = "#483D8B"
DARKSLATEGRAY = "#2F4F4F"
DARKTURQUOISE = "#00CED1"
DARKVIOLET = "#9400D3"
DEEPPINK = "#FF1493"
DEEPSKYBLUE = "#00BFFF"
DIMGRAY = "#696969"
DODGERBLUE = "#1E90FF"
FIREBRICK = "#B22222"
FLORALWHITE = "#FFFAF0"
FORESTGREEN = "#228B22"
FUCHSIA = "#FF00FF"
GAINSBORO = "#DCDCDC"
GHOSTWHITE = "#F8F8FF"
GOLD = "#FFD700"
GOLDENROD = "#DAA520"
GRAY = "#7F7F7F"
GREEN = "#008000"
GREENYELLOW = "#ADFF2F"
HONEYDEW = "#F0FFF0"
HOTPINK = "#FF69B4"
INDIANRED = "#CD5C5C"
INDIGO = "#4B0082"
IVORY = "#FFF0F0"
KHAKI = "#F0E68C"
LAVENDER = "#E6E6FA"
LAVENDERBLUSH = "#FFF0F5"
LAWNGREEN = "#7CFCF5"
LEMONCHIFFON = "#FFFACD"
LIGHTBLUE = "#ADD8E6"
LIGHTCORAL = "#F08080"
LIGHTCYAN = "#E0FFFF"
LIGHTGOLDENRODYELLOW = "#FAFAD2"
LIGHTGREEN = "#90EE90"
LIGHTGRAY = "#D3D3D3"
LIGHTPINK = "#FFB6C1"
LIGHTSALMON = "#FFA07A"
LIGHTSEAGREEN = "#20B2AA"
LIGHTSKYBLUE = "#87CEFA"
LIGHTSLATEGRAY = "#778899"
LIGHTSTEELBLUE = "#B0C4DE"
LIGHTYELLOW = "#FFFFE0"
LIME = "#00FF00"
LIMEGREEN = "#32CD32"
LINEN = "#FAF0E6"
MAGENTA = "#FF00FF"
MAROON = "#800000"
MEDIUMAQUAMARINE = "#66CDAA"
MEDIUMBLUE = "#0000CD"
MEDIUMORCHID = "#BA55D3"
MEDIUMPURPLE = "#9370DB"
MEDIUMSEAGREEN = "#3CB371"
MEDIUMSLATEBLUE = "#7B68EE"
MEDIUMSPRINGGREEN = "#00FA9A"
MEDIUMTURQOISE = "#48D1CC"
MEDIUMVIOLETRED = "#C71585"
MIDNIGHTBLUE = "#191970"
MINTCREAM = "#F5FFFA"
MISTYROSE = "#FFE4E1"
MOCCASIN = "#FFE1B5"
NAVAJOWHITE = "#FFDEAD"
NAVY = "#000080"
OLDLACE = "#FDF5E6"
OLIVE = "#808000"
OLIVEDRAB = "#6B8E23"
ORANGE = "#FFA500"
ORANGERED = "#FF4500"
ORCHID = "#DA7AD6"
PALEGOLDENROD = "#EEE8AA"
PALEGREEN = "#98FB98"
PALETURQOISE = "#AFEEEE"
PALEVIOLETRED = "#DB7093"
PAPAYAWHIP = "#FFEFD5"
PEACHPUFF = "#FFDAB9"
PERU = "#CD853F"
PINK = "#FFC0CB"
PLUM = "#D3A0DD"
POWDERBLUE = "#B0E0E6"
PURPLE = "#800080"
RED = "#FF0000"
ROSYBROWN = "#BC8F8F"
ROYALBLUE = "#4169E1"
SADDLEBROWN = "#8B4513"
SALMON = "#FA8072"
SANDYBROWN = "#F4A460"
SEAGREEN = "#2E8B57"
SEASHELL = "#FFF5EE"
SIENNA = "#A0522D"
SILVER = "#C0C0C0"
SKYBLUE = "#87CEEB"
SLATEBLUE = "#6A5ACD"
SLATEGRAY = "#708090"
SNOW = "#FFFAFA"
SPRINGGREEN = "#00FF7F"
STEELBLUE = "#4682B4"
TAN = "#D2B48C"
TEAL = "#008080"
THISTLE = "#D8BFD8"
TOMATO = "#FD6347"
TURQUOISE = "#40E0D0"
VIOLET = "#EE82EE"
WHEAT = "#F5DEAA"
WHITE = "#FFFFFF"
WHITESMOKE = "#F5F5F5"
YELLOW = "#FFFF00"
YELLOWGREEN = "#9ACD32"


def from_str(string):
    """
    Returns a color value from a color name.
    """
    try:
        return globals()[string]
    except KeyError:
        raise KeyError(
            "Please enter a supported color. Color name must be in all caps."
        )


def available(names_only=False):
    """
    Returns a list of currently available colors.
    """
    lst = []

    for key, value in globals().items():
        if (not key.startswith("__")) and key == key.upper():
            if names_only:
                entry = str(key)
            else:
                entry = f"{key}: {value}"

            lst.append(entry)

    return lst


def rgb_to_hex(*args):
    """
    Converts RGB values to a HEX string.
    Accepts three tuples or three passed parameters.
    """
    try:
        if len(args) == 1:
            args = tuple(n for n in args[0])
        return "#%02X%02X%02X" % args

    except Exception:
        raise TypeError(
            "Input must be a tuple. Either a single passed tuple, or exactly three passed params."
        )


def hex_to_rgb(hex_string):
    """
    Converts a HEX string into an RGB three tuple. Leading # is optional.
    """
    try:
        if hex_string.startswith("#"):
            hex_string = hex_string[1:]
    except TypeError:
        raise TypeError("Input must be a string")

    return tuple(int(hex_string[i : i + 2], 16) for i in (0, 2, 4))


def __rgbify():
    """
    Set all the color values to RGB tuples for use in pygame.
    INTERNAL USE ONLY
    """
    if type(from_str("BLACK")) is tuple:
        raise TypeError("Already RGB")

    for color_name in available(names_only=True):
        hex_val = from_str(color_name)
        globals()[color_name] = hex_to_rgb(hex_val)
