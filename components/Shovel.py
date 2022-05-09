import random

import pygame
from pygame.math import Vector3, Vector2


class Shovel(pygame.sprite.Sprite):

    def __init__(self, group, name, node, ton_per_pass, efficiency):
        super().__init__(group)
        self.render = group
        self.name = name
        self.node = node
        self.pos = self.render.drawables[self.node].get_coords()
        self.real_position = self.render.drawables[self.node].get_coords() + Vector3(-20, -20, 0)
        self.image = pygame.image.load('resources/shovel.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 20))
        self.rect = self.image.get_rect(center=Vector2(self.real_position.x, self.real_position.y))

        self.efficiency = efficiency
        self.ton_per_pass = ton_per_pass * self.efficiency
        self.queue_dict = {}
        self.is_loading = False
        self.load_time = 0
        self.current_loading_time = 0
        self.current_load = 0
        self.current_truck = None
        self.current_truck_payload = None
        self.material_spot_type = self.render.drawables[self.node].material

    def update(self):
        if not self.is_loading:
            self.render.hang += self.render.animation_speed/1000
            self.render.score -= 0.5*self.render.animation_speed/1000

    def set_load_time(self, truck_id, payload):
        self.current_loading_time = 0
        self.current_load = 0
        self.is_loading = True
        self.current_truck = truck_id
        self.current_truck_payload = payload
        self.load_time = random.uniform(0.016, 0.058)

    def add_load_time(self, timedelta):
        if self.current_load >= self.current_truck_payload:
            self.is_loading = False
            self.current_truck = None
            return
        self.current_loading_time += timedelta * self.load_time
        if self.current_loading_time >= self.load_time:
            self.current_load += random.uniform(0.85 * self.ton_per_pass, 1.15 * self.ton_per_pass)
            self.current_loading_time = 0
