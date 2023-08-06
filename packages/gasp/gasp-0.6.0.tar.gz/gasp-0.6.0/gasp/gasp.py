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

"""Publicly accessible API of GASP.

GASP is designed to be imported with `from gasp import *`.

To use any methods in this application, you must first run `begin_graphics()`.
"""

import random
import tkinter
import time

from . import color  # Default to HEX

_root_window = None

_canvas = None
_canvas_xs = None
_canvas_ys = None
_canvas_col = None
_canvas_tsize = 12
_canvas_tserifs = 0
_canvas_tfonts = ["times", "lucidasans-24"]

_mouse_enabled = 0
_mouse_x = None
_mouse_y = None

speed = 100  # set default game play speed to 100

_returning = 0


# === Time support ===========================================================


def sleep(secs):
    if _root_window is None:
        time.sleep(secs)
    else:
        _root_window.update_idletasks()
        _root_window.after(int(1000 * secs), _root_window.quit)
        _root_window.mainloop()


# === Initialization =========================================================


def begin_graphics(width=640, height=480, background=color.WHITE, title="GASP"):
    global _root_window, _canvas, _canvas_xs, _canvas_ys

    # Check for duplicate call
    if _root_window is not None:
        _root_window.destroy()

    # Save the canvas size parameters
    _canvas_xs, _canvas_ys = width - 1, height - 1

    # Create the root window
    _root_window = tkinter.Tk()
    _root_window.protocol("WM_DELETE_WINDOW", _destroy_window)
    _root_window.title(title)
    _root_window.resizable(0, 0)

    # Create the canvas object
    try:
        _canvas = tkinter.Canvas(
            _root_window, width=width, height=height, bg=background
        )
        _canvas.pack()
        _canvas.update()
    except:
        _root_window.destroy()
        _root_window = None

    # Bind to key-down and key-up events
    _root_window.bind("<KeyPress>", _keypress)
    _root_window.bind("<KeyRelease>", _keyrelease)
    _root_window.bind("<FocusIn>", _clear_keys)
    _root_window.bind("<FocusOut>", _clear_keys)
    _clear_keys()


def _destroy_window(event=None):
    global _root_window
    _root_window.destroy()
    _root_window = None


# === End graphics ===========================================================


def end_graphics():
    """
    Program terminated. Wait for graphics window to be closed.
    """
    global _root_window, _canvas, _mouse_enabled
    try:
        sleep(1)
        _root_window.destroy()
    finally:
        _root_window = None
        _canvas = None
        _mouse_enabled = 0
        _clear_keys()


# === Object drawing  ========================================================


class Plot:
    """Plot a point on the screen."""

    def __init__(self, pos, color=color.BLACK, size=1):
        self.pos = pos
        self.color = color
        self.size = size
        self.coord_list = [
            pos[0] - size,
            _canvas_ys - pos[1] - size,
            pos[0] + size,
            _canvas_ys - pos[1] + size,
        ]

        # Draw a small circle
        self.id = _canvas.create_oval(*self.coord_list, outline=color, fill=color)
        _canvas.update()

    def __repr__(self):
        return f"<Plot object at ({self.pos[0]}, {self.pos[1]})>"


class Line:
    """Draw a line segment between p1 and p2."""

    def __init__(self, start, end, color=color.BLACK, thickness=3):
        self.pos = start
        self.rise = end[0] - start[0]
        self.run = end[1] - start[1]
        self.coord_list = [start[0], _canvas_ys - start[1], end[0], _canvas_ys - end[1]]

        self.id = _canvas.create_line(*self.coord_list, fill=color, width=thickness)
        _canvas.update()

    def __repr__(self):
        return (
            f"<Line segment object from ({self.pos[0]}, {self.pos[1]})"
            f" to ({self.pos[0] + self.rise}, {self.pos[1] + self.run})>"
        )


class Box:
    """Draw a rectangle given lower right corner and width and height."""

    def __init__(
        self, corner, width, height, filled=False, color=color.BLACK, thickness=1
    ):
        self.pos = corner
        self.width = width
        self.height = height
        self.color = color
        self.filled = filled
        self.thickness = thickness
        self.coord_list = [
            corner[0],
            _canvas_ys - corner[1],
            corner[0] + width,
            _canvas_ys - corner[1] - height,
        ]

        fill = color if filled else ""  # transparent

        self.id = _canvas.create_rectangle(*self.coord_list, fill=fill, width=thickness)
        _canvas.update()

    def __repr__(self):
        return (
            f"<Box object {self.width} wide and {self.height} high at "
            f"({self.pos[0]}, {self.pos[1]})>"
        )


class Circle:
    """Draw a circle centered at the given coordinates with the given radius."""

    def __init__(self, center, radius, filled=False, color=color.BLACK, thickness=1):
        self.x = center[0]
        self.y = center[1]
        self.pos = center
        self.radius = radius
        self.color = color
        self.filled = filled
        self.thickness = thickness

        x0 = self.x - self.radius
        y0 = self.y - self.radius
        x1 = self.x + self.radius
        y1 = self.y + self.radius

        self.coord_list = [x0, _canvas_ys - y0, x1, _canvas_ys - y1]

        fill = color if filled else ""

        self.id = _canvas.create_oval(
            *self.coord_list, outline=color, fill=fill, width=thickness
        )
        _canvas.update()

    def __repr__(self):
        return f"<Circle object centered at ({self.pos[0]}, {self.pos[1]}) with a radius of {self.radius}>"


class Arc:
    """
    Draws an arc (essentially a wedge-shaped slice taken out of an ellipse)
    using the provided coords and radius.
    The start and end angle parameters change how large the "slice" is,
    measured in degrees (counter-clockwise) from the +x axis.
    """

    def __init__(
        self,
        center,
        radius,
        start_angle=0,
        end_angle=90,
        filled=False,
        color=color.BLACK,
        thickness=1,
        style=tkinter.ARC,
    ):
        self.pos = center
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.color = color
        self.style = style

        x1 = center[0] - radius
        y1 = center[1] - radius
        x2 = center[0] + radius
        y2 = center[1] + radius

        self.coord_list = [x1, _canvas_ys - y1, x2, _canvas_ys - y2]

        fill = color if filled else ""

        self.id = _canvas.create_arc(
            *self.coord_list,
            start=start_angle,
            extent=end_angle - start_angle,
            outline=color,
            fill=fill,
            width=thickness,
            style=style,
        )
        _canvas.update()

    def __repr__(self):
        return (
            f"<Arc object centered at {self.pos} with a radius of {self.radius}. "
            f"Its arc goes from {self.start_angle}º to {self.end_angle}º>"
        )


class Polygon:
    """
    Draws a polygon with the given coordinates. There must be three or more points.
    Connects the points in order left to right
    """

    def __init__(self, points, filled=False, color=color.BLACK, thickness=1):
        self.points = points
        self.filled = filled
        self.color = color
        self.thickness = thickness

        x_vals, y_vals = [], []
        x_sum, y_sum = 0, 0
        for pt in points:
            x_vals.append(pt[0])
            x_sum += pt[0]
            y_vals.append(pt[1])
            y_sum += pt[1]

        self.pos = (x_sum / len(x_vals), y_sum / len(y_vals))

        self.coord_list = [
            min(x_vals),
            _canvas_ys - min(y_vals),
            max(x_vals),
            _canvas_ys - max(y_vals),
        ]

        fill = color if filled else ""

        self.id = _canvas.create_polygon(
            *self.points, fill=fill, outline=color, width=thickness
        )
        _canvas.update()

    def __repr__(self):
        coords = ", ".join(map(str, [self.points[i] for i in range(len(self.points))]))
        return f"<A Polygon object with {len(self.points)} points, at {coords}>"


class Text:
    """Create a text box displaying the given string."""

    def __init__(self, text, pos, color=color.BLACK, size=12):
        self.text = text
        self.pos = pos
        self.size = size
        self.color = color

        self.coord_list = []  # TODO

        self.id = _canvas.create_text(
            self.pos[0], _canvas_ys - self.pos[1], text=self.text, fill=self.color
        )
        _canvas.update()

    def __repr__(self):
        return f'<A text box located at {self.pos}, with the text "{self.text}">'


# === Object moving and removing =============================================


def clear_screen(background=None):
    # Remove all drawn items
    _canvas.delete("all")

    # Change background color if requested
    if background is not None:
        _canvas.configure(bg=background)


def remove_from_screen(obj):
    _canvas.delete(obj.id)
    _root_window.tk.dooneevent(tkinter._tkinter.DONT_WAIT)


def move_by(obj, x, y):
    """Translate each x coordinate right and each y coordinate up"""

    _canvas.move(obj.id, x, -y)  # relative move

    obj.pos = (obj.pos[0] + x, obj.pos[1] + y)

    # c = obj.coord_list

    # obj.coord_list = [c[i] + x if i % 2 == 0 else c[i] - y for i in range(len(c))]

    # obj.pos = (obj.coord_list[0], _canvas_ys - obj.coord_list[1])

    _root_window.tk.dooneevent(tkinter._tkinter.DONT_WAIT)


def move_to(obj, p):
    dx = p[0] - obj.pos[0]
    dy = p[1] - obj.pos[1]
    move_by(obj, dx, dy)
    # there is a moveto function in tkinter, but it doesnt seem to work as intended


# === Keypress handling  =====================================================


def set_speed(speed_value):
    global speed
    speed = speed_value


# We bind to key-down and key-up events.
_keysdown = {}
# This holds an unprocessed key release.  We delay key releases by up-to
# one call to keys_pressed() to get round a problem with auto repeat.
_got_release = None


def _keypress(event):
    global _got_release
    _keysdown[event.keysym] = True
    _got_release = None


def _keyrelease(event):
    global _got_release
    try:
        del _keysdown[event.keysym]
    except Exception:
        pass
    _got_release = True


def _clear_keys(event=None):
    global _keysdown, _got_release
    _keysdown = {}
    _got_release = None


def keys_pressed():
    _root_window.tk.dooneevent(tkinter._tkinter.DONT_WAIT)

    if _got_release:
        _root_window.tk.dooneevent(tkinter._tkinter.DONT_WAIT)

    return _keysdown.keys()


def update_when(timing):
    global speed

    if timing == "key_pressed":
        keys = keys_pressed()
        while len(keys) == 0:
            keys = keys_pressed()

        _clear_keys()
        return list(keys)[0]

    elif timing == "next_tick":
        time.sleep(5 / speed)

    elif timing == "brief_check":
        keys = keys_pressed()

        start_t = time.time()
        end_t = time.time()

        while end_t - start_t < 0.05:
            end_t = time.time()
            keys = keys_pressed()

            if len(keys) != 0:
                return list(keys)[0]

        return []

    else:
        raise ValueError(
            "Invalid timing option. Use 'key_press' or 'next_tick' or 'brief_check'"
        )
