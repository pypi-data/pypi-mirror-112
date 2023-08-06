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

# GASP games module built on Pygame 2.0
# Developed by Richard Martinez

"""Publicly accessible API of GASP.

GASP games is designed to be imported with `from gasp import games`.

To use any methods in this application, you must preface it with '`games.`'.
"""


# Generic Error Class
class GamesError(Exception):
    pass


import math
from . import color

color.__rgbify()  # Make it RGB

# Silence Pygame Import in Terminal
from contextlib import redirect_stdout as __silence_pygame

with __silence_pygame(None):
    # Version 2.0.0
    try:
        import pygame
        from pygame.locals import *  # Imports constants for easy use (e.g. K_a, HWSURFACE, and RLEACCEL)
    except ModuleNotFoundError:
        raise GamesError(
            "Pygame is not installed. Please see the documentation for guidance on how to do that: "
            "http://openbookproject.net/pybiblio/gasp/"
        )

    pygame.init()
    pygame.font.init()

# ------------------------------------------------------------------------------


class Screen:
    """
    The Screen object represents the playing area. Since we can have only one
    screen under pygame, it's just a handy container for stuff.
    """

    initialised = 0
    got_statics = 0

    def __init__(self, width=640, height=480, title="GASP Games"):
        self.init_screen(width, height, title)

    def init_screen(self, width=640, height=480, title="GASP Games"):
        """
        width -- width of graphics window
        height -- height of graphics window
        """
        # Don't allow more than one window at once: pygame can only have one window
        if Screen.initialised:
            raise GamesError("Cannot have more than one Screen object")

        Screen.initialised = 1

        # Create the pygame display
        self._display = pygame.display.set_mode((width, height), HWSURFACE)
        self._width = width
        self._height = height
        self._background = self._display.convert()
        self.title = title
        self.set_title(title)
        self.set_background_color(color.BLACK)  # Remove screen tears on Mac

        # Initialise a list of objects in play
        self._objects = []
        # Initialise list dirty rectangles to be repainted
        self._dirtyrects = []

        # Time when we should draw the next frame
        self._next_tick = 0

    def __repr__(self):
        return f'<Screen "{self.title}" as ({self._width} x {self._height})>'

    def is_pressed(self, key):
        """
        Return true if the indicated key is pressed, false if not.
        The key should be specified using a pygame key identifier
        (defined in pygame.locals, and hence here, with a name
        beginning "K_").
        """
        # Add support for passing key as a string?
        return pygame.key.get_pressed()[key]

    def set_background(self, background):
        """
        Set the background to the surface provided. Note that the
        surface should not have transparency set, or weird things
        will happen.
        """
        # Reset current BG
        self._background = pygame.Surface((self._width, self._height))

        # Blit new BG as many times as needed to fill the screen
        # In case new BG is smaller than the screen
        for x in range(0, self._width, background.get_width()):
            for y in range(0, self._height, background.get_height()):
                self._background.blit(background, (x, y))

        # Blit new BG onto the display
        self._display.blit(self._background, (0, 0))
        pygame.display.update()

    def set_background_color(self, color):
        """
        Set the background to a surface consisting of the color
        provided.  Strange things will happen should the color
        have transparency!
        """
        # Color is RGB
        self._background = pygame.Surface((self._width, self._height))
        self._background.fill(color)
        self._display.blit(self._background, (0, 0))
        pygame.display.update()

    def set_title(self, title):
        pygame.display.set_caption(title)

    ##### Start methods to be overridden #####
    def tick(self):
        """
        If you override the tick method in a subclass of the Screen
        class, you can specify actions which are carried out every
        tick.
        """
        pass

    def keypress(self, key):
        """
        If you override the keypress method, you will be able to
        handle individual keypresses instead of dealing with the
        keys held down as in the standard library.
        """
        pass

    def mouse_down(self, pos, button):
        """
        This method will be called when a mouse button becomes
        pressed. You can override it if you want to make use of
        the information. By default, it does nothing.
        It will be passed two arguments. The first is the
        position of the mouse when the button is pressed,
        as a tuple (x,y). The second is the button number,
        starting at 0.
        """
        pass

    def mouse_up(self, pos, button):
        """
        This method will be called when a mouse button becomes
        un-pressed. You can override it if you want to make use of
        the information. By default, it does nothing.
        It will be passed two arguments. The first is the
        position of the mouse when the button is released,
        as a tuple (x,y). The second is the button number,
        starting at 0.
        """
        pass

    ##### End methods to be overridden #####

    def mouse_position(self):
        """
        Return the current position of the mouse as (x,y).
        """
        return pygame.mouse.get_pos()

    def mouse_buttons(self):
        """
        Return the current pressed-ness of up to three mouse buttons
        as a tuple (left,middle,right).
        """
        # num_buttons is new in pygame 2.0.0 but 3 is the old behavior
        return pygame.mouse.get_pressed(num_buttons=3)

    def handle_events(self):
        """
        If you override this method in a subclass of the Screen
        class, you can specify how to handle different kinds of
        events.  However you must handle the quit condition!
        """
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                self.quit()
            elif event.type == KEYDOWN:
                self.keypress(event.key)
            elif event.type == MOUSEBUTTONUP:
                self.mouse_up(event.pos, event.button - 1)
            elif event.type == MOUSEBUTTONDOWN:
                self.mouse_down(event.pos, event.button - 1)

    def quit(self):
        """
        Calling this method will stop the main loop from running and
        make the graphics window disappear.
        """
        self._exit = 1

    def clear(self):
        """
        Destroy all objects on this Screen.
        """
        for object in self._objects[:]:
            object.destroy()
        self._objects = []

    def _update_display(self):
        """
        Get the actual display in sync with reality.
        """
        pygame.display.update(self._dirtyrects)
        self._dirtyrects = []

    def mainloop(self, fps=50):
        """
        Run the pygame main loop. This will animate the objects on the
        screen and call their tick methods every tick.

        fps -- target frame rate
        """
        self._exit = 0

        while not self._exit:
            # Should there be a way to retrieve the screen's framerate?
            self._wait_frame(fps)

            for object in self._objects:
                if not object._static:
                    object._erase()
                    object._dirty = 1

            for object in self._objects[:]:
                if object._tickable:
                    object._tick()

            self.tick()

            if Screen.got_statics:
                for object in self._objects:
                    if not object._static:
                        for o in object.overlapping_objects():
                            if o._static and not o._dirty:
                                o._erase()
                                o._dirty = 1

            for object in self._objects:
                if object._dirty:
                    object._draw()
                    object._dirty = 0

            self._update_display()

            self.handle_events()

        # Throw away any pending events
        pygame.event.get()

    def _wait_frame(self, fps):
        """
        Wait for the correct fps time to expire.
        """
        this_tick = pygame.time.get_ticks()
        if this_tick < self._next_tick:
            pygame.time.delay(int(self._next_tick + 0.5) - this_tick)
        self._next_tick = this_tick + (1000.0 / fps)

    def overlapping_objects(self, rectangle):
        """
        Returns a list of all the objects which overlap the rectangle given.

        Rectangle must be in form: (left, top, width, height) or ((left, top), (width, height))
        """
        rect = pygame.Rect(rectangle)

        rect_list = []
        for obj in self._objects:
            rect_list.append(obj._rect)

        indices = rect.collidelistall(rect_list)

        over_objects = []
        for index in indices:
            over_objects.append(self._objects[index])

        return over_objects

    def all_objects(self):
        """
        Returns a list of all the Objects on the Screen.
        """
        return self._objects[:]

    def _raise(self, it, above=None):
        """
        Raise an object to the top of the stack, or above the specified object.
        """
        # This makes sure we're always in a consistent state
        objects = self._objects[:]
        # Remove the object from the list
        objects.remove(it)
        if above is None:
            # Put it on top (the end)
            objects.append(it)
        else:
            # Put the object after <above>
            idx = 1 + objects.index(above)
            objects[idx:idx] = [it]

        # Install the new list
        self._objects = objects

        # Force a redraw
        if it._static:
            it._erase()
            it._dirty = 1

    def _lower(self, it, below=None):
        """
        Lower an object to the bottom of the stack, or below the specified
        object.
        """
        # This makes sure we're always in a consistent state
        objects = self._objects[:]
        objects.remove(it)
        if below is None:
            # Put the object on the beginning (bottom) of the list
            self._objects = [it] + objects
        else:
            # Put the object before <below>
            idx = objects.index(below)
            objects[idx:idx] = [it]
            self._objects = objects

    def _raise_list(self, objects, above=None):
        """
        Raise all the objects in a list to the top of the stack,
        or above the specified object (which must not be in the list).
        """
        # Could be a simple for loop?
        # for object in objects:
        #     self._raise(object, above)

        # Filter out objects not in the given list
        new_objects = []
        for object in self._objects:
            if object not in objects:
                new_objects.append(object)

        # Put the list in the right place
        if above:
            idx = new_objects.index(above) + 1
        else:
            idx = len(new_objects)
        new_objects[idx:idx] = objects

        # And install
        self._objects = new_objects

    def _lower_list(self, objects, below=None):
        """
        Lower all the objects in a list to the bottom of the stack,
        or below a specified object (which must not be in the list).
        """
        # Could be a simple for loop?
        # for object in objects:
        #     self._lower(object, below)

        # Filter out objects not in the given list
        new_objects = []
        for object in self._objects:
            if object not in objects:
                new_objects.append(object)

        # Put the list in the right place
        if below:
            idx = new_objects.index(below)
        else:
            idx = 0
        new_objects[idx:idx] = objects

        # And install
        self._objects = new_objects

    def add_object(self, object):
        self._objects.append(object)

    def remove_object(self, object):
        try:
            self._objects.remove(object)
        except ValueError:
            # Silence errors
            # Already done it: happens in some games, not an error.
            pass

    def blit_and_dirty(self, source_surf, dest_pos):
        """
        You probably won't need to use this method in your own programs,
        as |Object| and its sub-classes know how to draw themselves on
        the screen. You'd need to use method if you wanted to draw an
        image on the screen which wasn't an |Object|.
        This method blits (draws, taking account of transparency) the
        given source surface |source_surf| to the screen at the position
        given by |dest_pos|.
        It then remembers the place where the surface was drawn as
        ``dirty''.  This means that when the display is updated on the
        next tick, this part of it will be redrawn.
        """
        rect = self._display.blit(source_surf, dest_pos)
        self._dirtyrects.append(rect)

    def blit_background(self, rect):
        """
        This method draws the background over the given rectangle, and
        marks that rectangle as ``dirty'' (see the |blit_and_dirty|
        method for what that means). It's used to erase an object before
        moving it. You shouldn't need to call it yourself.
        """
        try:
            rect = self._display.blit(self._background, rect, rect)
            self._dirtyrects.append(rect)
        except pygame.error:  # Objects were causing error on closing
            pass

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def center_pos(self):
        return self.get_width() // 2, self.get_height() // 2


# ------------------------------------------------------------------------------


class Object:
    """
    Object represents a graphical object on the screen. Objects can be moved,
    rotated, deleted, and maybe have other things done to them.
    Every object has a "reference point". When you move the object to a given point,
    it is moved so that its reference point ends up there.
    """

    def __init__(
        self, screen, x, y, surface, angle=0, x_offset=0, y_offset=0, static=0
    ):
        """
        Initialise the object:

        screen -- screen object to put the object on.
        x -- x pos of object's reference point.
        y -- y pos of object's reference point.
        surface -- pygame.Surface object.
        angle -- initial angle of rotation, in degrees.
        x_offset -- dx from reference point to BB top left at a=0.
        y_offset -- dy from reference point to BB top left at a=0.
        static -- flag, true if object usually doesn't need redrawing

        If you're using rather than writing the games
        module, then you almost certainly want to use one of the
        subclasses of Object rather than using Object itself.
        """
        self.screen = screen

        self._static = static
        if static:
            Screen.got_statics = 1

        self.screen.add_object(self)
        self._surface = surface
        self._orig_surface = surface  # Original surface before rotation
        self._orig_rect = surface.get_rect()

        # Offset from reference point to top left corner.
        self._x_offset_ = self._x_offset = x_offset
        self._y_offset_ = self._y_offset = y_offset

        self._rect = self._surface.get_rect()
        self._x = 0
        self._y = 0
        self.move_to(x, y)

        self._angle = angle
        if self._angle != 0:
            self._rotate()

        self._tickable = 0
        self._gone = 0
        self._dirty = 0

    def __del__(self):
        try:
            if not self._gone:
                self.destroy()
        except AttributeError:  # was raising errors
            pass

    def destroy(self):
        """
        Erase object from screen and remove it from the list of objects
        maintained by games module.
        """
        self._erase()
        if Screen.got_statics:
            for o in self.overlapping_objects():
                if o._static and not o._dirty:
                    o._erase()
                    o._dirty = 1

        self.screen.remove_object(self)
        self._gone = 1

    def _erase(self):
        """
        Erase object from screen by blitting the background over where it was.
        """
        self.screen.blit_background(self._rect)

    def _draw(self):
        """
        Draw object on screen by blitting the image onto the screen.
        """
        self.screen.blit_and_dirty(self._surface, self._rect)

    def replace_image(self, surface):
        """
        Remove the current surface defining the object and replace it with a new one.
        """
        self._orig_surface = surface
        self._orig_rect = surface.get_rect()

        if self._angle != 0:
            self._rotate()
        else:
            self._replace(surface)

    def _replace(self, surface):
        (x, y) = self.pos()
        self._surface = surface
        self._rect = self._surface.get_rect()
        self.move_to(x, y)

    def pos(self):
        return self._x, self._y

    def xpos(self):
        return self._x

    def ypos(self):
        return self._y

    def angle(self):
        return self._angle % 360

    def bbox(self):
        """Returns bounding box in form (left, top, width, height)"""
        return tuple(self._rect)

    def collidepoint(self, point):
        """
        Returns true if the given point overlaps the Object.
        """
        temp_rect = pygame.Rect(self.bbox())
        output = temp_rect.collidepoint(point)
        del temp_rect
        return output

    def move_to(self, x, y=None):
        """
        Move the object so that its reference point is at the given position.
        """
        if y is None:  # Passed as a two tuple
            x, y = x

        self._erase()
        self._dirty = 1

        self._x, self._y = x, y
        self._rect.left = int(x + self._x_offset)
        self._rect.top = int(y + self._y_offset)

    def move_by(self, dx, dy=None):
        """
        Move the object by the given amount.
        """
        if dy is None:  # Passed as a two tuple
            dx, dy = dx

        self.move_to(self._x + dx, self._y + dy)

    def rotate_to(self, angle):
        """
        Rotate the object to the given angle in degrees.

        Angles are with respect to the +x axis:
        Right -- 0 degrees
        Up -- 90 degrees
        Left -- 180 degrees
        Down -- 270 degrees
        """
        self._angle = angle % 360
        self._rotate()

    def rotate_by(self, angle):
        """
        Rotate the object by the given angle in degrees.
        """
        self.rotate_to(self._angle + angle)

    def _rotate(self):
        rotated_surface = pygame.transform.rotate(self._orig_surface, self._angle)
        self._replace(rotated_surface)
        self._rect = self._surface.get_rect()
        self._fix_offsets()
        self.move_to(self._x, self._y)

    def _set_offsets(self, x, y):
        self._x_offset_ = x
        self._y_offset_ = y
        self._fix_offsets()

    def _fix_offsets(self):
        if self._angle == 0:
            self._x_offset = self._x_offset_
            self._y_offset = self._y_offset_
        else:
            # Reference point to center of original rectangle
            dx = self._x_offset_ + (self._orig_rect.centerx - self._orig_rect.left)
            dy = self._y_offset_ + (self._orig_rect.centery - self._orig_rect.top)

            # Reference point to top left of new rectangle
            self._x_offset = dx - (self._rect.centerx - self._rect.left)
            self._y_offset = dy - (self._rect.centery - self._rect.top)

    def overlapping_objects(self):
        """
        Returns a list of objects that are overlapping the given object.
        """
        # Find approximate overlap list
        objects = self.screen.overlapping_objects(self._rect)
        if self in objects:
            objects.remove(self)
        for o in reversed(objects):
            if not self.overlaps(o):
                objects.remove(o)
        return objects

    def filter_overlaps(self, object):
        """
        This is a utility method which allows you to have
        better control over whether two objects have collided
        than just checking whether the rectangles which enclose
        them are touching. It is called after having
        established that the rectangles touch so you can assume
        that in your checking.
        Some subclasses of object override it (eg the |Circle|
        class). You can also override it in your own subclasses
        of |Object| to get better collision detection.
        This function should return 1 if the your object really
        overlaps the other object and 0 otherwise. The standard
        |Object| class just returns 1.
        """
        # Could maybe use pygame.mask module for this?
        return 1

    def overlaps(self, object):
        """
        Returns true if the passed object overlaps the given object. Otherwise, returns false.
        """
        return bool(
            self._rect.colliderect(object._rect)
            and self.filter_overlaps(object)
            and object.filter_overlaps(self)
        )

    def raise_object(self, above=None):
        """
        Raise an object to the top of the stack, or above the specified object.
        """
        self.screen._raise(self, above)

    def lower_object(self, below=None):
        """
        Lower an object to the bottom of the stack, or below the specified object.
        """
        self.screen._lower(self, below)

    def treat_as_dynamic(self):
        """
        Make the object not static. This is intended for temporary use for
        static objects that otherwise won't get redrawn correctly, such as
        the cursor on a board.
        """
        self._static = 0

    def treat_as_static(self):
        """
        Make the object static.  This is intended for undoing a previous
        call to treat_as_dynamic(), not as a way of making objects static
        as an afterthought.  In particular, it won't help if no static
        objects have been made up to this point.
        """
        self._static = 1


# ------------------------------------------------------------------------------


class Sprite(Object):
    """
    The class which lets you create sprites (that is, bitmaps).
    If you want a sprite that moves automatically, subclass from
    this and from Mover. If you want on that changes its image automatically,
    subclass from Animation instead of from Sprite.

    The reference point of a Sprite is the center of its bounding box.
    """

    def __init__(self, screen, x, y, image, angle=0, static=0):
        self.init_sprite(screen, x, y, image, angle, static)

    def init_sprite(self, screen, x, y, image, angle=0, static=0):
        """
        Arguments:

        screen -- the screen on which the sprite should appear.
        x -- the x-coordinate of the center of the image.
        y -- the y-coordinate of the center of the image.
        image -- the image object, as returned from the load_image function.
        angle -- the angle through which the image should be rotated.
        """
        Object.__init__(
            self,
            screen,
            x,
            y,
            image,
            angle,
            static=static,
            x_offset=-image.get_width() / 2,
            y_offset=-image.get_height() / 2,
        )

    def __repr__(self):
        return f"<Sprite at ({self.xpos()}, {self.ypos()})>"


# ------------------------------------------------------------------------------


class ColorMixin:
    """
    This is a mixin class which handles color changes for geometric objects
    by redrawing them on a new surface using their _create_surface method.
    """

    def set_color(self, color):
        if color != self._color:
            self._color = color
            if self._static:
                self._erase()
                self._dirty = 1
            surface = self._create_surface()
            self.replace_image(surface)

    def get_color(self):
        return self._color


# ------------------------------------------------------------------------------


class OutlineMixin:
    """
    This is a mixin class which handles color changes for the outlines of geometric objects
    by redrawing them on a new surface using their _create_surface method.
    """

    def set_outline(self, color):
        if color != self._outline:
            self._outline = color
            if self._static:
                self._erase()
                self._dirty = 1
            surface = self._create_surface()
            self.replace_image(surface)

    def get_outline(self):
        return self._outline


# ------------------------------------------------------------------------------


class Text(Object, ColorMixin):
    """
    A class for representing text on the screen.

    The reference point of a Text object is the center of its bounding box.
    """

    def __init__(self, screen, x, y, text, size, color, font=None, static=0):
        self.init_text(screen, x, y, text, size, color, font, static)

    def init_text(self, screen, x, y, text, size, color, font=None, static=0):
        """
        Arguments:

        screen -- the screen the object is on.
        x -- x-coordinate of center of bounding box.
        y -- y-coordinate of center of bounding box.
        text -- the text to display.
        size -- nominal height of the text, in pixels.
        color -- the color the text should be.
        """
        self._size = size
        self._color = color
        self._text = text
        self._assign_font(font)
        self._angle = 0
        surface = self._create_surface()
        Object.__init__(
            self,
            screen,
            x,
            y,
            surface,
            x_offset=self._x_offset,
            y_offset=self._y_offset,
            static=static,
        )
        self.move_to(x, y)

    def __repr__(self):
        return f'<Text "{self.get_text()}" at ({self.xpos()}, {self.ypos()}), color: {self.get_color()}>'

    def _create_surface(self):
        result = self._font.render(self._text, True, self._color)
        rect = result.get_rect()
        self._set_offsets(
            -0.5 * (rect.right - rect.left), -0.5 * (rect.bottom - rect.top)
        )
        return result

    def set_text(self, text):
        if text != self._text:
            self._erase()
            self._text = text
            surface = self._create_surface()
            self.replace_image(surface)

    def get_text(self):
        return self._text

    def set_font(self, font):
        self._assign_font(font)
        self._erase()
        surface = self._create_surface()
        self.replace_image(surface)

    @staticmethod
    def available_fonts():
        return pygame.font.get_fonts()

    def _assign_font(self, font):
        if font is None:  # Nothing passed
            self._font = pygame.font.Font(None, self._size)
        elif "." in font:  # Looks like a file name (.ttf)
            try:
                self._font = pygame.font.Font(font, self._size)
            except FileNotFoundError:
                raise GamesError(
                    "Invalid font path. Check to make sure the file path is correct."
                )
        else:  # Assume system font
            formatted = font.lower().replace(" ", "")

            if formatted in self.available_fonts():
                self._font = pygame.font.SysFont(formatted, self._size)
            else:  # Fall back on default font
                # This will save the day if someone uses a system font on their machine,
                # but it is not available when running on another machine.
                # Because of this, try to stick to basic fonts if you can.

                self._font = pygame.font.Font(None, self._size)

                # Tell the user that the font was not found
                print(f'\033[93mSystem font "{font}" was not found. Make sure your font is available with available_fonts()\033[0m')


# ------------------------------------------------------------------------------


class Line(Object, ColorMixin):
    """
    A line that is drawn on the screen. Its points are specified as a list of
    points relative to the line's reference point.
    """

    def __init__(self, screen, x, y, points, color, static=0, thickness=1):
        self.init_line(screen, x, y, points, color, static, thickness)

    def init_line(self, screen, x, y, points, color, static=0, thickness=1):
        """
        Arguments:

        screen -- the screen the object is on.
        x -- x-coordinate of reference point.
        y -- y-coordinate of reference point.
        points -- a list of points, each given as (dx,dy) from reference point.
        color -- color to draw the line.
        static -- whether or not the polygon is ever expected to move.
        thickness -- how thick the draw the line
        """
        self._color = color
        self.screen = screen  # Must do this here so surface convert works
        self._points = points
        self._angle = 0
        self._thickness = thickness

        surface = self._create_surface()
        Object.__init__(
            self,
            screen,
            x,
            y,
            surface,
            angle=self._angle,
            x_offset=self._x_offset,
            y_offset=self._y_offset,
            static=static,
        )

    def __repr__(self):
        return f"<Line at ({self.xpos()}, {self.ypos()}), color: {self._color}>"

    def set_points(self, points):
        self._points = tuple(points)
        old_x, old_y = self.pos()
        new_surf = self._create_surface()

        # The new surface may set new offsets, so ensure we
        # are just where we were:
        self.move_to(old_x, old_y)
        self.replace_image(new_surf)

    def get_points(self):
        return self._points

    def _create_surface(self):
        points = self._points

        minx = maxx = points[0][0]
        miny = maxy = points[0][1]

        for x, y in points:
            if x < minx:
                minx = x
            if x > maxx:
                maxx = x

            if y < miny:
                miny = y
            if y > maxy:
                maxy = y

        surface = pygame.Surface(
            (maxx - minx + 1 + self._thickness, maxy - miny + 1 + self._thickness)
        ).convert()

        # The part of the surface not occupied by the line should be
        # transparent. We choose a color that isn't the same as the color of the line
        key_color = (0, 0, 0)  # Default to black
        if self._color == key_color:  # Does this match?
            key_color = (0, 0, 10)  # Make it different

        surface.fill(key_color)
        surface.set_colorkey(key_color, RLEACCEL)

        start_pos = points[0]
        end_pos = points[1]

        # Offset from zero of user supplied co-ordinates to top left
        # of bounding box. These offsets are added to user-supplied coords
        # for move_to to give the new position of the top left of the surface.
        self._set_offsets(minx, miny)

        pygame.draw.line(
            surface, self._color, start_pos, end_pos, width=self._thickness
        )

        self._rect = surface.get_rect()

        return surface


# ------------------------------------------------------------------------------


class Polygon(Object, ColorMixin, OutlineMixin):
    """
    A polygon, either drawn in outline or filled in. Its shape is specified
    as a list of points relative to the polygon's reference point.
    """

    def __init__(
        self,
        screen,
        x,
        y,
        shape,
        color,
        filled=True,
        outline=None,
        static=0,
        thickness=1,
    ):
        self.init_polygon(
            screen, x, y, shape, color, filled, outline, static, thickness
        )

    def init_polygon(
        self,
        screen,
        x,
        y,
        shape,
        color,
        filled=True,
        outline=None,
        static=0,
        thickness=1,
    ):
        """
        Arguments:

        screen -- the screen the object is on.
        x -- x-coordinate of reference point.
        y -- y-coordinate of reference point.
        shape -- a list of vertices, each given as (dx,dy) from reference point.
        color -- color to draw either the boundary or the whole polygon.
        filled -- true if the polygon is to be filled in.
        outline -- color to draw the outline in (if different from whole polygon)
        static -- whether or not the polygon is ever expected to move
        """
        self._color = color
        self.screen = screen  # Must do this here so surface convert works
        self._filled = filled
        self._shape = tuple(shape)
        self._outline = outline
        self._angle = 0
        self._thickness = thickness

        surface = self._create_surface()
        Object.__init__(
            self,
            screen,
            x,
            y,
            surface,
            angle=0,
            x_offset=self._x_offset,
            y_offset=self._y_offset,
            static=static,
        )

    def __repr__(self):
        return f"<Polygon at ({self.xpos()}, {self.ypos()}), color: {self._color}, outline: {self._outline}>"

    def set_shape(self, shape):
        self._shape = tuple(shape)
        old_x, old_y = self.pos()
        new_surf = self._create_surface()

        # The new surface may set new offsets, so ensure we
        # are just where we were:
        self.move_to(old_x, old_y)
        self.replace_image(new_surf)

    def get_shape(self):
        return self._shape

    def _create_surface(self):

        shape = self._shape

        minx = maxx = shape[0][0]
        miny = maxy = shape[0][1]

        for x, y in shape:
            if x < minx:
                minx = x
            if x > maxx:
                maxx = x

            if y < miny:
                miny = y
            if y > maxy:
                maxy = y

        surface = pygame.Surface((maxx - minx + 1, maxy - miny + 1)).convert()

        # The part of the surface not occupied by the polygon should be
        # transparent. We choose a color that isn't the same as either of the ones
        # in which the polygon is to be drawn
        key_color = (0, 0, 0)  # Default to black
        if self._color == key_color or self._outline == key_color:  # Does this match?
            key_color = (0, 0, 10)  # Make it different
            if (
                self._color == key_color or self._outline == key_color
            ):  # Does it still match?
                key_color = (0, 10, 10)  # Now it has to be unique

        surface.fill(key_color)
        surface.set_colorkey(key_color, RLEACCEL)

        nshape = []
        for x, y in shape:
            nshape.append((x - minx, y - miny))
        nshape = tuple(nshape)

        # Offset from zero of user supplied co-ordinates to top left
        # of bounding box. These offsets are added to user-supplied coords
        # for move_to to give the new position of the top left of the surface.
        self._set_offsets(minx, miny)

        if self._filled:
            pygame.draw.polygon(surface, self._color, nshape, 0)
            if self._outline is not None:
                pygame.draw.polygon(surface, self._outline, nshape, self._thickness)
        elif self._outline is not None:
            pygame.draw.polygon(surface, self._outline, nshape, self._thickness)
        else:
            pygame.draw.polygon(surface, self._color, nshape, self._thickness)

        return surface


# ------------------------------------------------------------------------------


class Circle(Object, ColorMixin, OutlineMixin):
    """
    A circle, filled or otherwise, on the screen.
    The reference point is the center of the circle.
    """

    def __init__(
        self, screen, x, y, radius, color, filled=True, outline=None, static=0
    ):
        self.init_circle(screen, x, y, radius, color, filled, outline, static)

    def init_circle(
        self, screen, x, y, radius, color, filled=True, outline=None, static=0
    ):
        """
        Arguments:

        screen -- the screen the object is on.
        x -- x-coordinate of reference point.
        y -- y-coordinate of reference point.
        radius -- radius of the circle.
        color -- color to draw circle.
        filled -- whether or not to fill the circle with color.
        outline -- color to draw outline of circle.
        static -- whether or not the circle is ever expected to move
        """
        self._color = color
        self._outline = outline
        self.screen = (
            screen  # Must do this here so surface convert in _create_surface works
        )
        self._filled = filled
        self._radius = radius

        self._angle = 0

        surface = self._create_surface()
        Object.__init__(
            self,
            screen,
            x,
            y,
            surface,
            angle=0,
            x_offset=-radius,
            y_offset=-radius,
            static=static,
        )

    def __repr__(self):
        return f"<Circle at ({self.xpos()}, {self.ypos()}), radius: {self.get_radius()}, color: {self.get_color()}>"

    def _create_surface(self):
        surface = pygame.Surface((2 * self._radius + 1, 2 * self._radius + 1)).convert()

        key_color = (0, 0, 0)  # Default to black
        if self._color == key_color or self._outline == key_color:  # Does this match?
            key_color = (0, 0, 10)  # Make it different
            if (
                self._color == key_color or self._outline == key_color
            ):  # Does it still match?
                key_color = (0, 10, 10)  # Now it has to be unique

        surface.fill(key_color)
        surface.set_colorkey(key_color, RLEACCEL)

        self._set_offsets(-self._radius, -self._radius)

        if self._filled:
            pygame.draw.ellipse(surface, self._color, surface.get_rect(), 0)
            if self._outline is not None:
                pygame.draw.ellipse(surface, self._outline, surface.get_rect(), 1)
        elif self._outline is not None:
            pygame.draw.ellipse(surface, self._outline, surface.get_rect(), 1)
        else:
            pygame.draw.ellipse(surface, self._color, surface.get_rect(), 1)

        return surface

    def get_radius(self):
        return self._radius

    def set_radius(self, radius):
        if self._radius != radius:
            self._radius = radius
            surface = self._create_surface()
            self.replace_image(surface)

    def _rotate(self):
        pass  # To save processing power because a rotated circle is just itself

    def filter_overlaps(self, object):
        # Use pygame.mask module?
        rect = object._rect
        x0, y0, x1, y1 = rect.left, rect.top, rect.right, rect.bottom

        radius = self._radius
        radius2 = radius * radius

        x, y = self._x, self._y

        if x < x0 - radius or x > x1 + radius or y < y0 - radius or y > y1 + radius:
            return 0
        if x0 < x < x1 or y0 < y < y1:
            return 1
        if x < x0:
            if y < y0:
                return (x - x0) ** 2 + (y - y0) ** 2 <= radius2
            else:
                return (x - x0) ** 2 + (y - y1) ** 2 <= radius2
        else:
            if y < y0:
                return (x - x1) ** 2 + (y - y0) ** 2 <= radius2
            else:
                return (x - x1) ** 2 + (y - y1) ** 2 <= radius2


# ------------------------------------------------------------------------------


class Timer:
    """
    This is a class which you can add to an Object to make a new class.
    In your new class, you must supply a |tick| method. This method will
    be called every |interval| ticks, where |interval| is the argument you
    give to |init_timer|.
    """

    def __init__(self, interval=1, running=1):
        self.init_timer(interval, running)

        self._static = 1
        self._dirty = 0

    def init_timer(self, interval=1, running=1):
        """
        Call this function to start the timer. You must call it after
        the Object's init function.
        """
        self._interval = interval
        self._tickable = running
        self._next = 0

    def tick(self):
        pass

    def _tick(self):
        self._next += 1
        if self._next >= self._interval:
            self._next = 0
            self.tick()

    def get_interval(self):
        return self._interval

    def set_interval(self, interval):
        self._interval = interval

    def stop(self):
        self._tickable = 0

    def start(self):
        self._tickable = 1
        self._next = 0


# ------------------------------------------------------------------------------


class Mover(Timer):
    """
    This is a class which you can add to any Object or sub-class of
    Object to make a new class for something which moves itself around
    the screen. On each tick, your Object will be moved by the amount you specify.

    The moved method of your class will be called after each tick, even
    if the velocity of the object happens to be (0, 0).
    """

    def init_mover(self, dx, dy, da=0):
        """
        Call this to set up the Mover's speed after you've created it.
        Its Object init method (init_circle or whatever) must already have been called.
        """
        self.set_velocity(dx, dy)
        self.set_angular_speed(da)
        self.init_timer(1)

    def set_velocity(self, dx, dy=None):
        if dy is None:  # Passed as a two tuple
            dx, dy = dx

        self._dx = dx
        self._dy = dy

    def get_velocity(self):
        return self._dx, self._dy

    def set_angular_speed(self, da):
        self._da = da

    def get_angular_speed(self):
        return self._da

    def _tick(self):
        self.move_by(self._dx, self._dy)
        if self._da:
            self.rotate_by(self._da)
        self.moved()

    def moved(self):
        pass


# ------------------------------------------------------------------------------


class Message(Text, Timer):
    """
    A Text object that disappears from the screen after a while.
    More precisely, after a specified number of frames it will
    call the specified |after_death| function (if any) and then
    destroy itself.

    The reference point, as for the Text object, is the center
    of the bounding box.
    """

    def __init__(self, screen, x, y, text, size, color, lifetime, after_death=None):
        self.init_message(screen, x, y, text, size, color, lifetime, after_death)

    def init_message(self, screen, x, y, text, size, color, lifetime, after_death=None):
        """
        Arguments:

        x -- x-coordinate of center of bounding box.
        y -- y-coordinate of center of bounding box.
        text -- the text to display.
        size -- the size of the text, in pixels nominal height.
        color -- the color of the text.
        lifetime -- the number of frames to wait before disappearing.
        after_death -- the function to call immediately before disappearing.
        """
        self._after_death = after_death
        self.init_text(screen, x, y, text, size, color)
        self.init_timer(lifetime)

    def tick(self):
        if self._after_death:
            self._after_death()
        self.stop()
        self.destroy()


# ------------------------------------------------------------------------------


class Animation(Sprite, Timer):
    """
    An image that changes every N ticks.
    The init function expects (among other things) two lists of images.
    If the first list is [a,b,c,d] and the second is [x,y,z] then the
    sequence of images shown will be a,b,c,d, x,y,z, x,y,z, x,y,z, ... .
    The n_repeats parameter is the maximum number of images to show,
    or something <= 0 to keep showing for ever.
    You can give lists of filenames instead of lists of images,
    if you like.

    The reference point, as for a Sprite, is the center of the
    bounding box.
    """

    def __init__(
        self,
        screen,
        x,
        y,
        nonrepeating_images,
        repeating_images,
        n_repeats=0,
        repeat_interval=1,
        angle=0,
    ):
        self.init_animation(
            screen,
            x,
            y,
            nonrepeating_images,
            repeating_images,
            n_repeats,
            repeat_interval,
            angle,
        )

    # angle param is never used?
    def init_animation(
        self,
        screen,
        x,
        y,
        nonrepeating_images,
        repeating_images,
        n_repeats=0,
        repeat_interval=1,
        angle=0,
    ):
        """
        Arguments:

        screen -- the screen to put the image on.
        x -- the x-coordinate of the center of the image.
        y -- the y-coordinate of the center of the image.
        nonrepeating_images -- list of images to show just once each.
        repeating_images -- list of images to show cyclicly
          once nonrepeating_images have finished.
        n_repeats -- maximum number of images to show in total,
          or something <=0 to continue for ever.
        repeat_interval -- number of frames between image changes.
        angle -- angle to rotate through, in degrees.
        """
        if nonrepeating_images and type(nonrepeating_images[0]) is str:
            nonrepeating_images, repeating_images = load_animation(
                nonrepeating_images, repeating_images
            )

        self.nonrepeating_images = nonrepeating_images
        self.repeating_images = repeating_images
        self.n_repeats = n_repeats or -1

        self.started = 0
        first_image = self.next_image()
        if first_image is None:
            raise GamesError("An animation with no images is illegal.")

        Object.__init__(self, screen, x, y, first_image)
        self.init_timer(repeat_interval)

    def next_image(self):
        if self.n_repeats == 0:
            return None
        if self.n_repeats > 0:
            self.n_repeats -= 1
        if self.nonrepeating_images:
            return self.nonrepeating_images.pop(0)
        if not self.repeating_images:
            return None

        # Drag first item to back of the list
        self.repeating_images = self.repeating_images[1:] + [self.repeating_images[0]]
        if not self.started:  # Prevent list from being shifted the first time
            # Bring last item back to the front
            self.repeating_images = [self.repeating_images[-1]] + self.repeating_images[
                :-1
            ]
            self.started = 1

        return self.repeating_images[0]

    def tick(self):
        new_image = self.next_image()
        if new_image is None:
            self.destroy()
        else:
            self.replace_image(new_image)


# ------------------------------------------------------------------------------


# Utility Functions


def load_image(file, transparent=1):
    """
    Loads an image, prepares it for play. Returns a pygame.Surface object
    which you can give as the "image" parameter to Object.

    file -- the filename of the image to load
    transparent -- whether the background of the image should be transparent.
                   Defaults to true.
                   The background color is taken at the color of the pixel
                   at (0,0) in the image.
    """
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise GamesError(f'Could not load image "{file}" {pygame.get_error()}')

    if transparent:
        corner = surface.get_at((0, 0))
        surface.set_colorkey(corner, RLEACCEL)
    return surface.convert()


def load_sound(file):
    """
    Load a sound file, returning a Sound object.
    """
    try:
        return pygame.mixer.Sound(file)
    except pygame.error:
        return None


def load_animation(nonrepeating_files, repeating_files=None, transparent=1):
    """
    Loads a number of files. Returns the "nonrepeating images" and
    "repeating images" arguments needed for the Animation constructor.
    """
    if repeating_files is None:
        repeating_files = []

    nonrepeating = [load_image(file, transparent) for file in nonrepeating_files]
    repeating = [load_image(file, transparent) for file in repeating_files]

    return nonrepeating, repeating


def scale_image(image, x_scale, y_scale=None):
    """
    Return a version of the image that's been scaled by a factor
    x_scale in the x direction and y_scale in the y direction.
    If y_scale is not given, scale uniformly.
    """
    if y_scale is None:  # Uniform scaling
        y_scale = x_scale

    x_size, y_size = image.get_size()
    x_size *= x_scale
    y_size *= y_scale

    x_size, y_size = int(x_size), int(y_size)

    return pygame.transform.scale(image, (x_size, y_size))


def set_resolution(image, x_resolution=None, y_resolution=None):
    """
    Returns a version of the image that has the resolution desired. Similar to scale_image, but
    instead of scaling, it simply sets the desired resolution.
    """
    image_width = image.get_width()
    image_height = image.get_height()

    if x_resolution is None:
        x_resolution = image_width
    if y_resolution is None:
        y_resolution = image_height

    x_scale = x_resolution / image_width
    y_scale = y_resolution / image_height

    return scale_image(image, x_scale, y_scale)


def flip_image(image, vertical=False, horizontal=False):
    """
    Returns a version of the image that's been flipped vertically, horizontally, or both.
    """
    return pygame.transform.flip(image, horizontal, vertical)
