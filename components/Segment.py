
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
