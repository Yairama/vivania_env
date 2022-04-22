from copy import copy

import pygame, sys
from pygame.math import Vector2, Vector3

from components.Worker import Worker


class Truck(pygame.sprite.Sprite):
    def __init__(self, pos: Vector3, group, worker: Worker, efficiency: float, payload=200):
        super().__init__(group)
        self.image = pygame.image.load('resources/truck.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 50))
        self.pos = pos
        self.to = pos
        self.target_node = 'n1'
        self.old_pos = self.pos
        self.rect = self.image.get_rect(center=Vector2(self.pos.x, self.pos.y))
        self.direction = Vector2()
        self.speed = 25
        self.render = group
        self.payload = payload

        self.current_node_key = 'parking'
        self.next_node_key = 'parking'
        self.current_segment_key = ('parking', 'n1')
        self.path = []

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.move_to_node()
            #self.move(Vector3(320, 302, 0))

        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
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
        #print(self.pos, self.to)

        if self.pos == self.to:
            for key in drawables.keys():
                if type(key) == str:
                    if drawables[key].get_coords() == self.pos:
                        if self.current_node_key in self.path:
                            self.path.remove(self.current_node_key)
                        self.current_node_key = key
                        if len(self.path)>0:
                            self.next_node_key = self.path[0]
                            self.to = drawables[self.path.pop(0)].get_coords()
            print(self.current_node_key, self.next_node_key)

        if self.current_node_key != self.next_node_key:
            for key in drawables.keys():
                if type(key) == tuple:
                    if (key[0] == self.current_node_key or key[1] == self.current_node_key) and (key[0] == self.next_node_key or key[1] == self.next_node_key):
                        print(key)


        if (self.to - self.pos).magnitude() != 0:

            timedelta = self.render.get_animation_speed()
            timedelta /= 1000

            if ((self.to - self.pos).normalize() * timedelta * self.speed).length() < (
                    self.pos - self.to).length():
                self.old_pos = copy(self.pos)
                self.pos = self.pos + (self.to - self.pos).normalize() * timedelta * self.speed
                self.rect = self.image.get_rect(center=Vector2(self.pos.x, self.pos.y))
            else:
                self.old_pos = copy(self.pos)
                self.pos = self.to
                self.rect = self.image.get_rect(center=Vector2(self.pos.x, self.pos.y))


    def move(self, to: Vector3):
        self.to = to

    def move_to_node(self, to_node_key='n11'):
        self.path = self.render.find_path(self.current_node_key)[to_node_key]

