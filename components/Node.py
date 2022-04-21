import random

import pygame
from pygame.math import Vector3


class Node:

    def __init__(self, name: str, center: Vector3, neighboring_nodes: list):
        self.name = name
        self.neighboring_nodes = neighboring_nodes
        self.center = center

    def draw(self, internal_surface, offset):
        color = None
        if self.name[0] == 'n':
            color = '#8A2BE2'
        elif self.name[0] == 'c' and self.name[1] != 'r':
            color = '#7CFC00'
        else:
            color = '#EEE8AA'

        pygame.draw.circle(internal_surface, center=(self.center.x + offset[0], self.center.y + offset[1]), color=color,radius=10)

    def get_coords(self):
        return self.center

    def get_neighborhoods(self):
        return self.neighboring_nodes
