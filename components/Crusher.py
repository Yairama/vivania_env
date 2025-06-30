import random

import pygame
from pygame.math import Vector3, Vector2

from engine.RenderCore import RenderCore


class Crusher(pygame.sprite.Sprite):

    def __init__(self, group, name, node):
        super().__init__(group)
        self.render: RenderCore = group
        self.name = name
        self.node = node
        self.pos = self.render.drawables[self.node].get_coords()
        self.real_position = self.render.drawables[self.node].get_coords() + Vector3(-20, -20, 0)
        self.image = pygame.image.load('./resources/crusher.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=Vector2(self.real_position.x, self.real_position.y))

        self.queue_dict = {}
        self.is_dumping = False
        self.dump_time = 0
        self.current_dumping_time = 0
        self.current_load = 0
        self.current_truck = None
        self.type = 'crusher'


    def update(self):
        pass

    def set_dump_time(self, truck_id, current_load):
        self.current_dumping_time = 0
        self.is_dumping = True
        self.current_truck = truck_id
        self.current_load = current_load
        self.dump_time = random.uniform(0.008, 0.026)

    def add_dump_time(self, timedelta, material):
        self.current_dumping_time += timedelta * self.dump_time
        if self.current_dumping_time >= self.dump_time:
            if material == 'mineral':
                self.render.mineral_tonnes += self.current_load
                self.render.score += 4*self.current_load
                self.render.reward += 4 * self.current_load
            elif material == 'waste':
                self.render.waste_tonnes += self.current_load
                self.render.score -= 6*self.current_load
                self.render.reward -= 6*self.current_load
            self.current_load = 0
            self.current_dumping_time = 0
            self.is_dumping = False
            self.current_truck = None
