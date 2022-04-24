from copy import copy

import pygame, sys
from pygame.math import Vector2, Vector3

from components.Segment import Segment
from components.Worker import Worker


class Truck(pygame.sprite.Sprite):
    def __init__(self, pos: Vector3, group, truck_id: int, worker: Worker, efficiency: float, payload=200):
        super().__init__(group)
        self.image = pygame.image.load('resources/truck.png').convert_alpha()
        #self.image = pygame.transform.scale(self.image, (30 + (truck_id * truck_id), 20 + (truck_id * truck_id)))
        self.image = pygame.transform.scale(self.image, (30, 20))
        self.pos = pos
        self.to = pos
        self.truck_id = truck_id
        self.target_node = 'n1'
        self.old_pos = self.pos
        self.rect = self.image.get_rect(center=Vector2(self.pos.x, self.pos.y))
        self.direction = Vector2()
        self.speed = 25
        self.payload = payload
        self.is_load = False if payload == 0 else True
        self.efficiency = efficiency
        self.worker = worker

        self.render = group

        self.current_node_key = 'parking'
        self.next_node_key = 'parking'
        self.old_node_key = 'parking'
        self.current_segment_key = ('parking', 'n1')
        self.path = []

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            if True:
                self.move_to_node()
            # self.move(Vector3(320, 302, 0))

        elif keys[pygame.K_DOWN]:
            if self.truck_id == 2:
                self.move_to_node()
            # self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def update(self):
        self.input()

        drawables = self.render.get_drawables()

        # self.update_next_position(drawables)
        if self.pos == self.to:
            for key in drawables.keys():
                if type(key) == tuple:
                    if (key[0] == self.current_node_key or key[1] == self.current_node_key) and (
                            key[0] == self.old_node_key or key[1] == self.old_node_key):
                        drawables[key].remove_from_queue(self.truck_id, self.is_load)

                if type(key) == str:
                    if drawables[key].get_coords() == self.pos:
                        if self.current_node_key in self.path:
                            self.path.remove(self.current_node_key)
                        self.old_node_key = copy(self.current_node_key)
                        self.current_node_key = key
                        if len(self.path) > 0:
                            self.next_node_key = self.path[0]
                            self.to = drawables[self.path.pop(0)].get_coords()

        self.update_segment_parameters(drawables)

        if (self.to - self.pos).magnitude() != 0:
            timedelta = self.render.get_animation_speed()
            timedelta /= 1000
            speed = self.speed
            if ((self.to - self.pos).normalize() * timedelta * speed).length() < (
                    self.pos - self.to).length():
                self.old_pos = copy(self.pos)
                self.pos = self.pos + (self.to - self.pos).normalize() * timedelta * speed
                self.rect = self.image.get_rect(center=Vector2(self.pos.x, self.pos.y))
            else:
                self.old_pos = copy(self.pos)
                self.pos = self.to
                self.rect = self.image.get_rect(center=Vector2(self.pos.x, self.pos.y))

    def move(self, to: Vector3):
        self.to = to

    #    def update_next_position(self, drawables):

    def move_to_node(self, to_node_key='n11'):
        self.path = self.render.find_path(self.current_node_key)[to_node_key]

    def update_segment_parameters(self, drawables):
        if self.current_node_key != self.next_node_key:
            for key in drawables.keys():
                if type(key) == tuple:
                    if (key[0] == self.current_node_key or key[1] == self.current_node_key) and (
                            key[0] == self.next_node_key or key[1] == self.next_node_key):
                        self.update_speed(drawables[key])
                        drawables[key].update_queue(self.truck_id, self.speed, self.pos, self.is_load)

    def update_speed(self, segment: Segment):
        self.speed = segment.get_speeds()[0] * self.efficiency * self.worker.efficiency if self.is_load else \
            segment.get_speeds()[1] * self.efficiency * self.worker.efficiency

        if self.truck_id in segment.get_load_dic().keys() or self.truck_id in segment.get_empty_dic().keys():
            dic = segment.get_load_dic() if self.is_load else segment.get_empty_dic()
            truck_index = list(dic.keys()).index(self.truck_id)

            if (len(dic.keys()) > 1 and truck_index != 0 and list(dic.items())[truck_index - 1][1][0] < self.speed) or \
                    self.speed == 0:
                distance = (dic[self.truck_id][1] - list(dic.items())[truck_index - 1][1][1]).magnitude()
                if distance < 5:
                    self.speed = 0
                elif 9 > distance >= 5:
                    self.speed = list(dic.items())[truck_index - 1][1][0]/2
                elif 15 >= distance >= 9:
                    self.speed = list(dic.items())[truck_index - 1][1][0]
                else:
                    self.speed = segment.get_speeds()[0] * self.efficiency * self.worker.efficiency if self.is_load \
                        else segment.get_speeds()[1] * self.efficiency * self.worker.efficiency

            if truck_index == 0:
                self.speed = segment.get_speeds()[0] * self.efficiency * self.worker.efficiency if self.is_load else \
                    segment.get_speeds()[1] * self.efficiency * self.worker.efficiency

    def set_payload(self, payload):
        self.payload = payload
        self.is_load = False if payload == 0 else True

    def get_id(self):
        return self.truck_id
