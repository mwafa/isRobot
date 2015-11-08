from __future__ import division

import pygame
from math import pi
from random import random

from arena import Arena, ARENA_MARKINGS_COLOR, ARENA_MARKINGS_WIDTH, \
                    CORNER_COLOURS, fade_to_white
from ..markers import Token

def token_positions(separation):
    offsets = (-separation, 0, separation)
    for x_pos in offsets:
        for y_pos in offsets:
            yield x_pos, y_pos

class SunnySideUpArena(Arena):
    start_locations = [(-3.6, -3.6),
                       ( 3.6, -3.6),
                       ( 3.6,  3.6),
                       (-3.6,  3.6)]

    start_headings = [0.25*pi,
                      0.75*pi,
                      -0.75*pi,
                      -0.25*pi]

    starting_zone_side = 1
    scoring_zone_side = 2

    def __init__(self, objects=None, wall_markers=True):
        super(SunnySideUpArena, self).__init__(objects, wall_markers)

        for i, pos in enumerate(token_positions(separation = 1.5)):
            token = Token(self, i, damping=10)
            token.location = pos
            self.objects.append(token)

    def draw_background(self, surface, display):
        super(SunnySideUpArena, self).draw_background(surface, display)

        def get_coord(x, y):
            return display.to_pixel_coord((x, y), self)

        def towards_zero(point, dist):
            if point < 0:
                return point + dist
            else:
                return point - dist

        # Lines separating zones
        def line(start, end):
            pygame.draw.line(surface, ARENA_MARKINGS_COLOR, \
                             start, end, ARENA_MARKINGS_WIDTH)

        def starting_zone(x, y):
            length = self.starting_zone_side
            a = get_coord(towards_zero(x, length), y)
            b = get_coord(x, towards_zero(y, length))
            c = (a[0], b[1])

            line(a, c)
            line(b, c)

        def scoring_zone(corner_pos, colour):
            x, y = corner_pos
            length = self.scoring_zone_side
            a = get_coord(towards_zero(x, length), y)
            b = get_coord(x, towards_zero(y, length))
            c = get_coord(x, y)

            pygame.draw.polygon(surface, colour, (a, b, c), 0)

        for i, pos in enumerate(self.corners):
            colour = fade_to_white(CORNER_COLOURS[i])
            scoring_zone(pos, colour)
            starting_zone(*pos)
