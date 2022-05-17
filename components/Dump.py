import random

import pygame
from pygame.math import Vector3, Vector2

from engine.RenderCore import RenderCore


class Dump(pygame.sprite.Sprite):

    def __init__(self, group, name, node):
        super().__init__(group)
        self.render: RenderCore = group
        self.name = name
        self.node = node
        self.pos = self.render.drawables[self.node].get_coords()
        self.real_position = self.render.drawables[self.node].get_coords() + Vector3(-20, -20, 0)
        self.image = pygame.image.load('vivania_env/resources/dump.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=Vector2(self.real_position.x, self.real_position.y))

        self.type = 'dump_zone'
        self.trucks_times = {}

    def update(self):
        pass

    def set_dump_time(self, truck_id, load, material):
        self.trucks_times[truck_id] = [0, random.uniform(0.008, 0.026), True, load, material]

    def add_dump_time(self, truck_id, timedelta):
        self.trucks_times[truck_id][0] += timedelta * self.trucks_times[truck_id][1]
        if self.trucks_times[truck_id][0] >= self.trucks_times[truck_id][1]:
            if self.trucks_times[truck_id][4] == 'waste':
                self.render.waste_tonnes += self.trucks_times[truck_id][3]
                self.render.score += self.trucks_times[truck_id][3]
                self.render.reward += self.trucks_times[truck_id][3]
            elif self.trucks_times[truck_id][4] == 'mineral':
                self.render.mineral_tonnes += self.trucks_times[truck_id][3]
                self.render.score -= 3.*self.trucks_times[truck_id][3]
                self.render.reward -= 3. * self.trucks_times[truck_id][3]
            self.trucks_times[truck_id] = [0, random.uniform(0.008, 0.026), False, 0, 'none']
