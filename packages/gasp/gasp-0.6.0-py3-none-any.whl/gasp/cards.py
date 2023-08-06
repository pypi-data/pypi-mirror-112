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

# GASP cards module
# Developed by Richard Martinez

"""Publicly accessible API of GASP.

GASP cards is designed to be imported with `from gasp import cards`.

To use any methods in this application, you must preface it with '`cards.`'.
"""

from gasp import games
from gasp import color
from gasp.utils import add_vectors, distance
from random import sample
import pygame

pygame.font.init()

# Ace, 2-10, Jack, Queen, King
VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

# Spades, Hearts, Diamonds, Clubs
SUITS = ["S", "H", "D", "C"]

# Contains all the codes for a deck
# A code contains a value and a suit
# e.g Ace of Spades would be "AS"
# 3 of Hearts would be "3H"
# 7 of Clubs would be "7C" etc.
CODES = []
for suit in SUITS:
    for value in VALUES:
        entry = value + suit
        CODES.append(entry)

SPADES = CODES[0:13]
HEARTS = CODES[13:26]
DIAMONDS = CODES[26:39]
CLUBS = CODES[39:52]

# Generic Font used in _get_text_surface
_FONT = pygame.font.SysFont("", 35)

# Coordinate positions of where to draw suit surfaces on each value card
_SUIT_POSITIONS = {
    "A": [(40, 60)],
    "2": [(40, 20), (40, 100)],
    "3": [(40, 20), (40, 100), (40, 60)],
    "4": [(20, 20), (20, 100), (60, 20), (60, 100)],
    "5": [(20, 20), (20, 100), (60, 20), (60, 100), (40, 60)],
    "6": [(20, 20), (20, 100), (20, 60), (60, 20), (60, 100), (60, 60)],
    "7": [(20, 20), (20, 100), (20, 60), (60, 20), (60, 100), (60, 60), (40, 50)],
    "8": [(20, 20), (20, 100), (20, 60), (60, 20), (60, 100), (60, 60), (40, 50), (40, 70)],
    "9": [(20, 12), (20, 44), (20, 76), (20, 108), (60, 12), (60, 44), (60, 76), (60, 108), (40, 60)],
    "10": [(30, 22), (20, 44), (20, 76), (30, 98), (50, 22), (60, 44), (60, 76), (50, 98), (40, 50), (40, 70)],
    "J": [(40, 60)],
    "Q": [(40, 60)],
    "K": [(40, 60)],
}


def _encode(value, suit):
    """
    Encodes a value and a suit for internal use
    """
    return value + suit


def _decode(code):
    """
    Decodes an internal code.
    """
    value = code[:-1]
    suit = code[-1]
    return value, suit


def get_suit_color(code):
    """
    Returns the color of the suit passed.
    Works with full codes or just suits
    """
    for suit in ["S", "C"]:
        if suit in code:
            return color.BLACK

    for suit in ["H", "D"]:
        if suit in code:
            return color.RED


def _get_text_surface(text, color):
    """
    Returns only the surface needed to draw text.
    """
    return _FONT.render(text, True, color)


def _get_suit_surface(suit):
    """
    Returns only the surface needed to draw the suits.
    """
    suit_color = get_suit_color(suit)

    surface = pygame.Surface((40, 40)).convert()
    key_color = color.PURPLE
    surface.fill(key_color)
    surface.set_colorkey(key_color, pygame.RLEACCEL)

    if suit == "S":  # Spades
        radius = 10

        pos = (radius, 20)
        pygame.draw.circle(surface, suit_color, pos, radius)

        pos = (40 - radius, 20)
        pygame.draw.circle(surface, suit_color, pos, radius)

        points = [(20, 0), (40, 20), (0, 20)]
        pygame.draw.polygon(surface, suit_color, points)

        points = [(20, 20), (30, 40), (10, 40)]
        pygame.draw.polygon(surface, suit_color, points)
    elif suit == "H":  # Hearts
        radius = 10

        pos = (radius, radius)
        pygame.draw.circle(surface, suit_color, pos, radius)

        pos = (3 * radius, radius)
        pygame.draw.circle(surface, suit_color, pos, radius)

        points = [(0, radius), (40, radius), (20, 40)]
        pygame.draw.polygon(surface, suit_color, points)
    elif suit == "D":  # Diamonds
        points = [(20, 0), (35, 20), (20, 40), (5, 20)]
        pygame.draw.polygon(surface, suit_color, points)
    elif suit == "C":  # Clubs
        radius = 8

        pos = (20, radius)
        pygame.draw.circle(surface, suit_color, pos, radius)

        pos = (radius, 20)
        pygame.draw.circle(surface, suit_color, pos, radius)

        pos = (40 - radius, 20)
        pygame.draw.circle(surface, suit_color, pos, radius)

        points = [(20, 10), (28, 40), (10, 40)]
        pygame.draw.polygon(surface, suit_color, points)
    else:
        return

    surface = games.set_resolution(
        surface, 20, 20
    )  # Draw at a higher res then scale down
    return surface


class Card(games.Sprite):
    """
    A standard playing card on the screen.
    """

    def __init__(self, screen, x, y, code, size=70):
        self.init_card(screen, x, y, code, size)

    def init_card(self, screen, x, y, code, size=70):
        """
        Arguments:

        screen -- the screen on which this card lives
        x, y -- the screen coordinates of the center of the card
        code -- a string encoding the value and suit of the card
        size -- the height of the card in pixels
        """
        if code not in CODES:
            raise games.GamesError("Please enter a valid card code.")

        self.code = code
        self.value, self.suit = _decode(self.code)
        self.color = get_suit_color(self.code)
        self.size = size
        self.facing_up = True
        self.deck = None

        image, backside = self._create_surface()
        self._image = games.set_resolution(
            image, x_resolution=size * (5 / 7), y_resolution=size
        )
        self._backside = games.set_resolution(
            backside, x_resolution=size * (5 / 7), y_resolution=size
        )
        self.init_sprite(screen, x, y, self._image)

    def __repr__(self):
        return f"<Card {self.code} at ({self.xpos()}, {self.ypos()})>"

    def flip(self):
        """
        Flips the card over to reveal its opposite side.
        If the card is facing up, the backside will be revealed and vice versa.
        """
        self.facing_up = not self.facing_up

        if self.facing_up:
            self.replace_image(self._image)
        else:
            self.replace_image(self._backside)

    def _create_surface(self):
        """
        Creates the surfaces needed to draw the card.
        """
        # Setup surface
        s_width = 100
        s_height = 140
        surface = pygame.Surface((s_width, s_height)).convert()

        key_color = color.PURPLE
        surface.fill(key_color)
        surface.set_colorkey(key_color, pygame.RLEACCEL)

        # Make the card white
        surface.fill(color.WHITE)

        # Get the number surface
        number = _get_text_surface(self.value, self.color)

        # Top left number
        pos = (5, 5)
        surface.blit(number, pos)

        # Bottom right number
        pos = (95 - number.get_width(), 135 - number.get_height())
        surface.blit(number, pos)

        # Add suit surface
        suit_surface = _get_suit_surface(self.suit)
        # pos = (40, 60)
        for pos in _SUIT_POSITIONS[self.value]:
            surface.blit(suit_surface, pos)

        temp_rect = pygame.Rect(0, 0, 100, 140)
        pygame.draw.rect(surface, color.DIMGRAY, temp_rect, width=5)

        # Setup backside
        backside = pygame.Surface((s_width, s_height)).convert()

        key_color = color.PURPLE
        backside.fill(key_color)
        backside.set_colorkey(key_color, pygame.RLEACCEL)

        # Draw the backside
        backside.fill(color.RED)

        down_right = (100, -80), (0, 20)
        down_left = (0, -80), (100, 20)
        offset = (0, 30)

        # Draw the lines on the back
        for i in range(7):  # Perfect number of times to cover backside
            for line in [down_right, down_left]:
                pygame.draw.line(backside, color.WHITE, line[0], line[1], width=3)

            down_right = add_vectors(down_right[0], offset), add_vectors(
                down_right[1], offset
            )
            down_left = add_vectors(down_left[0], offset), add_vectors(
                down_left[1], offset
            )

        pygame.draw.rect(backside, color.DIMGRAY, temp_rect, width=5)

        del temp_rect
        return surface, backside

    def get_overlapping_cards(self, codes_only=False):
        """
        Returns a list of cards that are overlapping the selected card.
        If |codes_only| is True, the list will return the codes of all overlapped cards.
        """
        lst = []
        for object in self.overlapping_objects():
            try:
                if object.code in CODES:  # Is a card
                    if codes_only:
                        lst.append(object.code)
                    else:
                        lst.append(object)
            except AttributeError:
                pass
        return lst

    def get_above(self):
        """
        Returns the card immediately above.
        If no card, returns None.
        """
        if self.deck is None:
            raise games.GamesError("get_above only works for Cards in a Deck.")

        all_objects = self.screen.all_objects()
        index = all_objects.index(self)

        while True:  # do this as many times as necessary
            try:
                index += 1
                above = all_objects[index]
                if above not in self.deck.stack:
                    continue

                if not self.overlaps(above):
                    continue
            except IndexError:
                return None

            return above

    def get_below(self):
        """
        Returns the card immediately below.
        If no card, returns None.
        """
        if self.deck is None:
            raise games.GamesError("get_below only works for Cards in a Deck.")

        all_objects = self.screen.all_objects()
        index = all_objects.index(self)

        while True:  # do this as many times as necessary
            try:
                index -= 1
                below = all_objects[index]
                if below not in self.deck.stack:
                    continue

                if not self.overlaps(below):
                    continue

                if index < 0:  # Don't loop around
                    raise IndexError
            except IndexError:
                return None

            return below


class Deck:
    """
    A standard deck of 52 playing cards.
    A container for |Card| objects.
    """

    def __init__(self, screen, x, y, size=70, facing_up=True):
        self.init_deck(screen, x, y, size, facing_up)

    def init_deck(self, screen, x, y, size=70, facing_up=True):
        """
        Arguments:

        screen -- the screen on which this deck lives
        x, y -- the screen coordinates in which to draw the deck's center
        size -- the height of the cards in pixels
        facing_up -- determines the starting direction of the cards in the deck
        """
        self.screen = screen
        self.size = size
        self.start_x = x
        self.start_y = y
        self.stack = []  # Analogous to boards grid
        for code in reversed(CODES):
            card = self.new_card(x, y, code)
            card.deck = self
            self.stack.append(card)

        if not facing_up:
            for card in self.stack:
                card.flip()

    def __repr__(self):
        return f"<Deck at ({self.start_x}, {self.start_y}), size: {self.size}>"

    def new_card(self, x, y, code):
        return Card(self.screen, x, y, code, self.size)

    def shuffle(self, lst=None):
        """
        Shuffles a list of cards. By default, shuffles the whole deck.
        This works best before any of the cards have been moved, or if
        all of the cards are in the same location.
        """
        if lst is None:
            lst = self.stack

        lst = sample(lst, len(lst))
        for card in lst:
            card.raise_object()

    def get_card(self, code):
        """
        Returns the card object in the deck with the correct |code|.
        """
        if code not in CODES:
            raise games.GamesError("Please enter a valid card code.")

        for card in self.stack:
            if card.code == code:
                return card

    def get_hovered(self, pos):
        """
        Returns the card which is raised highest on the screen at |pos|.
        Will return None if no card is found.
        """
        for object in reversed(self.screen.all_objects()):
            if object in self.stack:
                if object.collidepoint(pos):
                    return object


class SingleDeck(Deck, games.Screen):
    """
    A subclass of |Deck| and |Screen| which automatically
    handles card movement using the mouse.
    This is probably the easiest way to use the cards module.
    """

    def __init__(
        self, x, y, size=70, facing_up=True, width=640, height=480, title="GASP Games"
    ):
        self.init_singledeck(x, y, size, facing_up, width, height, title)

    def init_singledeck(
        self, x, y, size=70, facing_up=True, width=640, height=480, title="GASP Games"
    ):
        """
        Arguments:

        x, y -- the screen coordinates in which to draw the deck's center
        size -- the height of the cards in pixels
        facing_up -- determines the starting direction of the cards in the deck
        width -- the width of the screen
        height -- the height of the screen
        title -- the title of the window as a string
        """
        self.init_screen(width, height, title)
        self.init_deck(self, x, y, size, facing_up)
        self.grabbing = False
        self.current_card = None

        # Some values only needed internally. Not recommended to touch these
        # mouse_dx, mouse_dy, previous right click frame
        self.__internals = [None, None, self.mouse_buttons()[2]]

    def tick(self):
        self.handle_cards()

    def handle_cards(self, allow_flipping=False, auto_raise=True):
        """
        Automatically handle card movement using the mouse.
        If |allow_flipping| is True, then right-clicking on a card will flip it.
        |auto_raise| ensure that the current card is raised to the top of the screen.
        """
        if self.mouse_buttons()[0]:  # Left Click
            if not self.grabbing:
                # Go from the top down (highest raised card)
                card = self.get_hovered(self.mouse_position())
                if card is not None:
                    self.grabbing = True
                    self.current_card = card
                    if auto_raise:
                        self.current_card.raise_object()
                    self.on_card_grab()

                    # Setup internal values for movement with respect to mouse
                    current_pos = self.current_card.pos()
                    mouse_pos = self.mouse_position()
                    self.__internals[0] = mouse_pos[0] - current_pos[0]
                    self.__internals[1] = mouse_pos[1] - current_pos[1]
        else:
            self.grabbing = False

        if self.grabbing:
            # Move cards with respect to the mouse
            x, y = self.mouse_position()
            dx, dy = self.__internals[:2]
            self.current_card.move_to(x - dx, y - dy)

        if allow_flipping:
            # Right Click but only on mouse_up
            if not self.mouse_buttons()[2] and self.__internals[2]:
                card = self.get_hovered(self.mouse_position())
                if card is not None:
                    self.current_card = card
                    self.current_card.flip()
                    if auto_raise:
                        self.current_card.raise_object()

            # Setup interval values for Right Click but only on mouse_up
            self.__internals[2] = self.mouse_buttons()[2]

    def on_card_grab(self):
        """
        Gets called only on the first frame of grabbing a card.
        Override this to do whatever you want.
        """
        pass


class Pile(games.Circle):
    """
    A place to put playing cards neatly.
    """

    def __init__(self, deck, x, y, color):
        self.init_pile(deck, x, y, color)

    def init_pile(self, deck, x, y, color):
        """
        Arguments:

        deck -- the deck that this pile is for
        x, y -- the center position of the pile
        color -- the color of the pile
        """
        self.deck = deck
        self.init_circle(deck.screen, x, y, radius=deck.size * 0.7, color=color)
        self.lower_object()

    def __repr__(self):
        return f"<Pile at ({self.pos()}, radius: {self.get_radius()})>"

    def clean_pile(self):
        """
        Neatly packs all cards within the pile's reach to its center.
        """
        for card in self.deck.stack:
            d = distance(self.pos(), card.pos())
            if d == 0:
                continue
            elif d < self.get_radius():
                card.move_to(self.pos())

    def get_cards(self, codes_only=False):
        """
        Returns a list of all cards currently in the pile ordered from the bottom up.
        |codes_only| is the same as in |get_overlapping_cards|.
        """
        sample_card = None
        for object in self.overlapping_objects():
            if object in self.deck.stack:
                if object.pos() == self.pos():  # Actually in the pile's center
                    sample_card = object
                    break

        if sample_card is None:  # Did not find a card in pile
            return []
        else:
            unordered_list = sample_card.get_overlapping_cards() + [sample_card]
            for card in unordered_list:
                if card.pos() != self.pos():
                    unordered_list.remove(card)

            ordered_list = []
            for object in self.screen.all_objects():
                if object in unordered_list:
                    ordered_list.append(object)

            if codes_only:
                ordered_list = [card.code for card in ordered_list]

            return ordered_list
