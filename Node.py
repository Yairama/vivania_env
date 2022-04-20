import random

import pygame


class Node:

    def __init__(self, name: str, x: int, y: int, z: int, neighboring_nodes: list):
        self.name = name
        self.neighboring_nodes = neighboring_nodes
        self.x = x
        self.y = y
        self.z = z

    def draw(self, scaled_surface, offset):
        color = None
        if self.name[0] == 'n':
            color = '#8A2BE2'
        elif self.name[0] == 'c' and self.name[1] != 'r':
            color = '#7CFC00'
        else:
            color = '#EEE8AA'

        pygame.draw.circle(scaled_surface, center=(self.x + offset[0], self.y + offset[1]), color=color, radius=10)
