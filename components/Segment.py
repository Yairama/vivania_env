
import pygame
from pygame.math import Vector3


class Segment:

    def __init__(self, start_point: Vector3, end_point: Vector3, empty_speed, load_speed, direction):
        self.start_point = start_point
        self.end_point = end_point
        self.distance = (end_point - start_point).magnitude()
        self.empty_speed = empty_speed
        self.load_speed = load_speed
        self.direction = direction
        self.a_dict = {}
        self.b_dict = {}
        self.first_loaded_truck_speed = 0
        self.first_empty_truck_speed = 0

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

    def get_speeds(self):
        return self.load_speed, self.empty_speed

    def update_queue(self, id_truck, speed, position, truck_direction):
        if truck_direction == self.direction:
            self.a_dict[id_truck] = (speed, position)
            self.first_loaded_truck_speed = list(self.a_dict.items())[0][1][0]
        elif truck_direction == (self.direction[1], self.direction[0]):
            self.b_dict[id_truck] = (speed, position)
            self.first_empty_truck_speed = list(self.b_dict.items())[0][1][0]

    def remove_from_queue(self, id_truck, truck_direction):
        if id_truck in self.a_dict.keys() or id_truck in self.b_dict.keys():
            if truck_direction == self.direction:
                self.a_dict.pop(id_truck)
            elif truck_direction == (self.direction[1], self.direction[0]):
                self.b_dict.pop(id_truck)

    def get_dic(self, truck_direction):

        if truck_direction == self.direction:
            return self.a_dict
        elif truck_direction == (self.direction[1], self.direction[0]):
            return self.b_dict
