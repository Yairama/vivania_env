
import pygame
from pygame.math import Vector3


class Segment:

    def __init__(self, start_point: Vector3, end_point: Vector3, empty_speed, load_speed):
        self.start_point = start_point
        self.end_point = end_point
        self.distance = (end_point - start_point).magnitude()
        self.empty_speed = empty_speed
        self.load_speed = load_speed

    def draw(self, internal_surface, offset):
        pygame.draw.line(internal_surface, color='#3443eb',
                         start_pos=(self.start_point.x + offset[0], self.start_point.y + offset[1]),
                         end_pos=(self.end_point.x + offset[0], self.end_point.y + offset[1]),
                         width=3)

    def is_on(self, c: Vector3):
        a = self.start_point
        b = self.end_point
        "Return true iff point c intersects the line segment from a to b."
        # (or the degenerate case that all 3 points are coincident)
        return (self.collinear(a, b, c)
                and (self.within(a.x, c.x, b.x) if a.x != b.x else
                     self.within(a.y, c.y, b.y)))

    def collinear(self, a, b, c):
        "Return true iff a, b, and c all lie on the same line."
        return (b.x - a.x) * (c.y - a.y) == (c.x - a.x) * (b.y - a.y)

    def within(self, p, q, r):
        "Return true iff q is between p and r (inclusive)."
        return p <= q <= r or r <= q <= p