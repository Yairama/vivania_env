import random

import pygame
from pygame.math import Vector3, Vector2


class Crusher(pygame.sprite.Sprite):

    def __init__(self, group, name, node, crusher_speed):
        super().__init__(group)
        self.render = group
        self.name = name
        self.node = node
        self.pos = self.render.drawables[self.node].get_coords()
        self.real_position = self.render.drawables[self.node].get_coords() + Vector3(-20, -20, 0)
        self.image = pygame.image.load('resources/crusher.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=Vector2(self.real_position.x, self.real_position.y))

        self.queue_dict = {}
        self.crusher_speed = crusher_speed
        self.is_dumping = False
        self.is_full = False
        self.dump_time = 0
        self.current_dumping_time = 0
        self.current_dump = 0
        self.current_load = 0
        self.current_truck = None
        self.type = 'crusher'

    def update(self):
        pass

    def set_dump_time(self, truck_id, current_load):
        self.current_dumping_time = 0
        if self.current_dump > 600:
            self.is_full = True
        self.is_dumping = True
        self.current_truck = truck_id
        self.current_load = current_load
        self.dump_time = random.uniform(0.008, 0.026)

    def add_dump_time(self, timedelta):
        self.current_dump -= timedelta*self.crusher_speed
        if self.current_dump <= 480:
            self.is_full = False
        if self.is_full:
            return

        if self.current_load == 0:
            self.is_dumping = False
            self.current_truck = None
            return
        self.current_dumping_time += timedelta * self.dump_time
        if self.current_dumping_time >= self.dump_time:
            self.current_load = 0
            self.current_dumping_time = 0
