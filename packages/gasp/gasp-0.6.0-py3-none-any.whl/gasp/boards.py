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

# GASP boards module
# Developed by Richard Martinez

"""Publicly accessible API of GASP.

GASP boards is designed to be imported with `from gasp import boards`.

To use any methods in this application, you must preface it with '`boards.`'.
"""


from . import games
from . import color
from pygame.locals import *
from gasp.utils import random_between

DEFAULT_LINE_COLOR = color.BLACK
DEFAULT_FILL_COLOR = color.LIGHTGRAY
DEFAULT_CURSOR_COLOR = color.RED

LEFT = 0
UP_LEFT = 1
UP = 2
UP_RIGHT = 3
RIGHT = 4
DOWN_RIGHT = 5
DOWN = 6
DOWN_LEFT = 7


def turn_45_clockwise(direction):
    return (direction + 1) % 8


def turn_45_anticlockwise(direction):
    return (direction - 1) % 8


def turn_90_clockwise(direction):
    return (direction + 2) % 8


def turn_90_anticlockwise(direction):
    return (direction - 2) % 8


def turn_180(direction):
    return (direction + 4) % 8


def random_direction(orthogonal_only=0):
    if orthogonal_only:
        return 2 * random_between(0, 3)
    return random_between(0, 7)


class GameCell(games.Polygon):
    """
    A square cell on a square grid (i.e., a GameBoard).
    In typical applications this will be subclassed.
    """

    def __init__(self, board, i, j, line_color=None, fill_color=None):
        self.init_gamecell(board, i, j, line_color, fill_color)

    def init_gamecell(self, board, i, j, line_color=None, fill_color=None):
        """
        Arguments:

        board -- The board this lives on.
        i -- Column number within the grid, starting at 0 at the left.
        j -- Row number within the grid, starting with 0 at the top.
        line_color -- Color of edges.
        fill_color -- Color of interior of cell.

        Creating grid cells is usually the job of the GridBoard
        object.
        """
        self.board = board

        # If no colors specified, use the board's color settings
        if line_color is None:
            line_color = self.board._line_color
        if fill_color is None:
            fill_color = self.board._fill_color

        self.screen_x, self.screen_y = board.cell_to_coords(i, j)
        box_size = board.box_size
        shape = (
            (0, 0),
            (0, box_size),
            (box_size, box_size),
            (box_size, 0),
        )  # Make a square
        self.init_polygon(
            board.screen,
            self.screen_x,
            self.screen_y,
            shape,
            fill_color,
            filled=True,
            outline=line_color,
            static=1,
        )

        self.neighbors = []
        self.direction = [None] * 8  # A list of 8 None values
        self.grid_x = i
        self.grid_y = j

    def raise_object(self, above=None):
        self.screen._raise(self, above)

        # Raise all non-grid type items
        for item in self.overlapping_objects():
            try:
                item.grid_x  # Is it a gridcell type?
            except AttributeError:
                item.raise_object()  # No? Raise it
            else:
                pass  # Yes? Pass

    def add_neighbor(self, neighbor):
        """
        What it says. Let this cell know that |neighbor| is one of
        its neighbors. This should be called for all pairs of cell
        when the grid is created. This establishes the connection
        only in one direction.
        """
        self.neighbors.append(neighbor)

    def add_direction(self, direction, cell):
        """
        Let this cell know that the |cell| given is in the direction
        |direction| from it.  This should be called for all appropriate
        pairs of cells when the grid is created, if the fast reference
        to neighboring cells is needed.  It is most often of use if
        the board wraps at the edges, so a piece going off the top
        reenters at the bottom.  This establishes the connection in
        one direction only.
        """
        self.direction[direction] = cell

    def grid_coords(self):
        """
        Returns the grid coordinates of the cell as a tuple.
        """
        return self.grid_x, self.grid_y

    def screen_coords(self):
        """
        Returns the screen coordinates of the cell as a tuple.
        """
        return self.screen_x, self.screen_y


class GameBoard:
    """
    A square grid of cells, each an instance of the GameCell class.
    Typically, GameBoard and GameCell will both be subclassed,
    and the new_gamecell method overridden so that it creates
    cells of the correct class.
    """

    def __init__(
        self,
        screen,
        origin,
        n_cols,
        n_rows,
        box_size,
        line_color=DEFAULT_LINE_COLOR,
        fill_color=DEFAULT_FILL_COLOR,
        cursor_color=DEFAULT_CURSOR_COLOR,
    ):
        self.init_gameboard(
            screen,
            origin,
            n_cols,
            n_rows,
            box_size,
            line_color,
            fill_color,
            cursor_color,
        )

    def init_gameboard(
        self,
        screen,
        origin,
        n_cols,
        n_rows,
        box_size,
        line_color=DEFAULT_LINE_COLOR,
        fill_color=DEFAULT_FILL_COLOR,
        cursor_color=DEFAULT_CURSOR_COLOR,
    ):
        """
        Arguments:

        screen -- The screen on which this board lives.
        origin -- A tuple (x,y) giving the coords of the top left corner.
        n_cols -- The number of columns in the grid.
        n_rows -- The number of rows in the grid.
        box_size -- The total width and height of each cell.
        line_color -- The color of the grid lines.
        fill_color -- The color of the interior of each cell.
        cursor_color -- The color in which the edges of a cell
                         should be highlighted when the "cursor"
                         is over it.

        Initially, there is no cursor.
        """
        self._origin = origin
        self._n_cols = n_cols
        self._n_rows = n_rows
        self.box_size = box_size
        self.grid = []
        self.cursor = None
        self.screen = screen

        self._line_color = line_color
        self._fill_color = fill_color
        self._cursor_color = cursor_color

        self.key_movements = {
            K_UP: (0, -1),
            K_DOWN: (0, 1),
            K_LEFT: (-1, 0),
            K_RIGHT: (1, 0),
        }

        for i in range(n_cols):
            self.grid.append([])
            for j in range(n_rows):
                if self.on_board(i, j):
                    self.grid[i].append(self.new_gamecell(i, j))
                else:
                    self.grid[i].append(None)

        self._outline_type = None

    def cell_to_coords(self, i, j):
        """
        Return the pixel coordinates of the top-left corner
        of the cell whose "board coordinates" are (i, j).
        """
        return self._origin[0] + i * self.box_size, self._origin[1] + j * self.box_size

    def coords_to_cell(self, x, y):
        """
        Return the "board coordinates" of the cell in which
        the point (x, y) in pixel coordinates lies.
        """
        # This is integer division.
        return (x - self._origin[0]) // self.box_size, (
            y - self._origin[1]
        ) // self.box_size

    def new_gamecell(self, i, j):
        """
        Create and return a new GameCell object at (i, j) in the grid.
        Subclass this if you need a proper subclass instead of GameCell instead.
        """
        return GameCell(self, i, j, self._line_color, self._fill_color)

    def create_neighbors(self, orthogonal_only=0):
        """
        Call the add_neighbor method for each pair of adjacent cells
        in the grid. If orthogonal_only is true, a cell has 4 neighbors;
        otherwise, 8 neighbors.
        """
        for i in range(self._n_cols):
            for j in range(self._n_rows):
                if not self.on_board(i, j):
                    continue
                for k in (-1, 0, 1):
                    for l in (-1, 0, 1):
                        if k == l == 0 or not self.on_board(i + k, j + l):
                            continue
                        if k != l and k != -l:
                            self.grid[i][j].add_neighbor(self.grid[i + k][j + l])
                        elif not orthogonal_only and k != 0 and l != 0:
                            self.grid[i][j].add_neighbor(self.grid[i + k][j + l])

    def create_directions(self, orthogonal_only=0, wrap=0):
        """
        Call the add_direction method for each pair of adjacent cells
        in the grid. If orthogonal_only is true, a cell has 4 neighbors;
        otherwise, 8 neighbors.  If wrap is true, a cell on the edge of
        the board has neighbors on the opposite edge, otherwise it has
        no neighbor in that direction.
        """
        # This method is kind of a mess mainly because of the ambiguous variable names.
        # Maybe it needs a makeover?
        for i in range(self._n_cols):
            for j in range(self._n_rows):
                if not self.on_board(i, j):
                    continue
                if i != 0 or wrap:
                    k = (i - 1) % self._n_cols
                    if self.on_board(k, j):
                        self.grid[i][j].add_direction(LEFT, self.grid[k][j])
                    if not orthogonal_only:
                        if j != 0 or wrap:
                            l = (j - 1) % self._n_rows
                            if self.on_board(k, l):
                                self.grid[i][j].add_direction(UP_LEFT, self.grid[k][l])
                        if j != self._n_rows - 1 or wrap:
                            l = (j + 1) % self._n_rows
                            if self.on_board(k, l):
                                self.grid[i][j].add_direction(
                                    DOWN_LEFT, self.grid[k][l]
                                )
                if i != self._n_cols - 1 or wrap:
                    k = (i + 1) % self._n_cols
                    if self.on_board(k, j):
                        self.grid[i][j].add_direction(RIGHT, self.grid[k][j])
                    if not orthogonal_only:
                        if j != 0 or wrap:
                            l = (j - 1) % self._n_rows
                            if self.on_board(k, l):
                                self.grid[i][j].add_direction(UP_RIGHT, self.grid[k][l])
                        if j != self._n_rows - 1 or wrap:
                            l = (j + 1) % self._n_rows
                            if self.on_board(k, l):
                                self.grid[i][j].add_direction(
                                    DOWN_RIGHT, self.grid[k][l]
                                )
                if j != 0 or wrap:
                    l = (j - 1) % self._n_rows
                    if self.on_board(i, l):
                        self.grid[i][j].add_direction(UP, self.grid[i][l])
                if j != self._n_rows - 1 or wrap:
                    l = (j + 1) % self._n_rows
                    if self.on_board(i, l):
                        self.grid[i][j].add_direction(DOWN, self.grid[i][l])

    def map_grid(self, fn):
        """
        Call fn for each cell in the grid.
        """
        for i in range(self._n_cols):
            for j in range(self._n_rows):
                if self.on_board(i, j):
                    fn(self.grid[i][j])

    def draw_all_outlines(self):
        """
        Sets the board to draw the outlines of all the cells in the board.
        Call this method somewhere in your |tick| function (preferably towards the end).
        """
        if self._outline_type == "limited":
            raise games.GamesError("This board already has limited outlines.")
        self._outline_type = "all"

        def make_dirty(o):
            o._dirty = 1

        self.map_grid(make_dirty)

    def limit_outlines(self, fn, true_color, false_color):
        """
        Sets the board to only draw the outlines of certain cells.
        For each box in the grid, if fn(box) returns True, the outline is set to |true_color|.
        Otherwise, it will be set to |false_color|.
        Call this method somewhere in your |tick| function (preferably towards the end).
        """
        if self._outline_type == "all":
            raise games.GamesError("This board already has all outlines.")
        self._outline_type = "limited"

        def apply(box):
            if fn(box):
                box.set_outline(true_color)
            else:
                box.set_outline(false_color)

        self.map_grid(apply)

    def keypress(self, key):
        """
        This should be called whenever a key is pressed.
        In any class that subclasses both GameBoard and Screen,
        this will happen automatically.

        By default, only the cursor is handled. If you override this method
        make sure you call |handle_cursor| somewhere in your method (probably at
        the beginning) if you still want the cursor to be handled.
        """
        self.handle_cursor(key)

    def on_board(self, i, j):
        """
        Return true if (i, j) is on the board, false otherwise.
        Override this to restrict which cells are created and are legal cursor positions.
        """
        return 0 <= i < self._n_cols and 0 <= j < self._n_rows

    def handle_cursor(self, key):
        """
        The handler method for the cursor. Call this somewhere in your |keypress|
        method if you want the cursor to be handled.
        """
        try:
            (dx, dy) = self.key_movements[key]

            if self.cursor is not None:
                (x, y) = (self.cursor.grid_x + dx, self.cursor.grid_y + dy)
                if self.on_board(x, y):
                    self.move_cursor(x, y)
        except (KeyError, AttributeError):
            pass

    def enable_cursor(self, i, j):
        """
        Nake there be a cursor, at (i, j) in grid coordinates.
        If there is already a cursor, it is simply moved to (i, j).
        """
        if self.cursor is None:
            self.cursor = self.grid[i][j]
            self.cursor.raise_object()
            self.cursor.set_outline(self._cursor_color)
            self.cursor.treat_as_dynamic()
            self.cursor_moved()
        else:
            self.move_cursor(i, j)

    def disable_cursor(self):
        """
        Make there be no cursor.
        """
        if self.cursor is not None:
            self.cursor.treat_as_static()
            self.cursor.raise_object()
            self.cursor.set_outline(self._line_color)
            self.cursor_moved()  # To reacquire visibility of contents
            self.cursor = None

    def move_cursor(self, i, j):
        """
        Make the cursor (which must already exist) be at (i, j) in grid coordinates.
        """
        self.cursor.treat_as_static()
        self.cursor.raise_object()
        self.cursor.set_outline(self._line_color)
        self.cursor = self.grid[i][j]
        self.cursor.raise_object()
        self.cursor.set_outline(self._cursor_color)
        self.cursor.treat_as_dynamic()
        self.cursor_moved()

    def cursor_moved(self):
        """
        Override this if you want to be notified if the cursor moves.
        """
        pass


class SingleBoard(GameBoard, games.Screen):
    """
    An almost trivial subclass of GameBoard and Screen,
    suitable for use when there is just one board which is
    the main thing on the screen.
    """

    def __init__(
        self,
        margins,
        n_cols,
        n_rows,
        box_size,
        line_color=DEFAULT_LINE_COLOR,
        fill_color=DEFAULT_FILL_COLOR,
        cursor_color=DEFAULT_CURSOR_COLOR,
        title="GASP Games",
    ):
        self.init_singleboard(
            margins,
            n_cols,
            n_rows,
            box_size,
            line_color,
            fill_color,
            cursor_color,
            title,
        )

    def init_singleboard(
        self,
        margins,
        n_cols,
        n_rows,
        box_size,
        line_color=DEFAULT_LINE_COLOR,
        fill_color=DEFAULT_FILL_COLOR,
        cursor_color=DEFAULT_CURSOR_COLOR,
        title="GASP Games",
    ):
        """
        Arguments:

        margins -- A tuple (x,y) giving the amount of space on each side:
                   x at left and right, y at top and bottom.
                   Or, a tuple (xL,yT,xR,yB) giving the amount on all four
                   sides separately: left, top, right, bottom.
                   Or, a single number that will be used for all margins.
        n_cols -- The number of columns in the grid.
        n_rows -- The number of rows in the grid.
        box_size -- The total width and height of each cell.
        line_color -- The color of the grid lines.
        fill_color -- The color of the interior of each cell.
        cursor_color -- The color in which the edges of a cell
                         should be highlighted when the "cursor"
                         is over it.

        Initially, there is no cursor.
        """
        try:
            left, top = margins[:2]
        except TypeError:
            left, top, margins = (
                margins,
                margins,
                (margins, margins),
            )  # Probably has to do with parsing

        if len(margins) == 2:
            right, bottom = margins
        else:
            right, bottom = margins[2:]

        self.init_screen(
            n_cols * box_size + left + right, n_rows * box_size + top + bottom, title
        )
        self.init_gameboard(
            self,
            (left, top),
            n_cols,
            n_rows,
            box_size,
            line_color,
            fill_color,
            cursor_color,
        )


class Container:
    def __init__(self, contents):
        self.init_container(contents)

    def init_container(self, contents):
        self._contents = contents

        for string in self._contents:
            setattr(self, string, None)

    def _items(self):
        return [getattr(self, string) for string in self._contents]

    def _apply(self, fn_name, *args, reverse=False):
        lst = self._items()

        if reverse:
            lst = reversed(lst)

        for item in lst:
            if item is None:
                continue

            try:
                fn = getattr(item, fn_name)
                fn(*args)
            except (AttributeError, TypeError):
                raise games.GamesError("Container Error")

    def move_to(self, x, y=None):
        # Might be a problem if contents are not overlapping
        # Use move_by to preserve relative distances between contents
        if y is None:  # Passed as a two tuple
            (x, y) = x
        self._apply("move_to", x, y)

    def move_by(self, dx, dy=None):
        if dy is None:
            (dx, dy) = dx
        self._apply("move_by", dx, dy)

    def raise_object(self, above=None):
        self._apply("raise_object", above)

    def lower_object(self, below=None):
        self._apply("lower_object", below, reverse=True)

    def destroy(self):
        self._apply("destroy")

    def pos(self):
        # Always return the position of the first item in the Container
        return self._items()[0].pos()

    def xpos(self):
        return self.pos()[0]

    def ypos(self):
        return self.pos()[1]

    def bbox(self):
        # Always the first item
        return self._items()[0].bbox()

    def angle(self):
        # Always the first item
        return self._items()[0].angle()

    def rotate_to(self, angle):
        self._apply("rotate_to", angle)

    def rotate_by(self, angle):
        self._apply("rotate_by", angle)

    def overlaps(self, object):
        return self._items()[0].overlaps(object)

    def overlapping_objects(self):
        lst = self._items()[0].overlapping_objects()

        for item in reversed(self._items()):
            if item in lst:
                lst.remove(item)

        return lst
