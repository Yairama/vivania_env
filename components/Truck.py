import math
from copy import copy

import numpy as np
import pygame, sys
from pygame.math import Vector2, Vector3

from components.Crusher import Crusher
from components.Dump import Dump
from components.Segment import Segment
from components.Text import Text
from engine.RenderCore import RenderCore


class Truck(pygame.sprite.Sprite):
    def __init__(self, pos: Vector3, group, truck_id: int, efficiency: float, payload=200):
        """

        :rtype: object
        """
        super().__init__(group)
        self.or_empty_image = pygame.image.load('vivania_env/resources/empty_truck2.png').convert_alpha()
        self.or_empty_image = pygame.transform.scale(self.or_empty_image, (30, 20))
        self.or_waste_load_image = pygame.image.load('vivania_env/resources/waste_loaded_truck.png').convert_alpha()
        self.or_waste_load_image = pygame.transform.scale(self.or_waste_load_image, (30, 20))
        self.or_mineral_load_image = pygame.image.load('vivania_env/resources/mineral_loaded_truck.png').convert_alpha()
        self.or_mineral_load_image = pygame.transform.scale(self.or_mineral_load_image, (30, 20))
        self.image = copy(self.or_empty_image)
        self.pos = pos
        self.to = pos
        self.truck_id = truck_id
        self.target_node = 'n1'
        self.old_pos = self.pos
        self.rect = self.image.get_rect(center=Vector2(self.pos.x, self.pos.y))
        self.orientation = None
        self.speed = 25
        self.payload = payload
        self.is_load = False
        self.efficiency = efficiency

        self.render: RenderCore = group
        self.current_node_key = 'parking'
        self.next_node_key = 'parking'
        self.old_node_key = 'parking'
        self.current_segment_key = ('parking', 'parking')
        self.path = []
        self.current_load = 0
        self.text = Text(self.render, f'{self.truck_id} - {self.current_load}', 10, '#831010', 40, 12, self.pos)
        self.material_type = None
        self.counter = 0
        self.is_loading = False
        self.is_dumping = False
        # self.direction = None
        # self.old_direction = None

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.counter += 1
            if self.counter == 1:
                self.move_to_node('c1')
            # self.move(Vector3(320, 302, 0))
        elif keys[pygame.K_DOWN]:
            self.counter += 1
            if self.counter == 1:
                self.move_to_node('n1')
        else:
            self.counter = 0

        # if keys[pygame.K_RIGHT]:
        #     pass
        # elif keys[pygame.K_LEFT]:
        #     pass
        # else:
        #     self.counter = 0

    def update(self):
        # self.input()

        drawables = self.render.drawables
        timedelta = self.render.get_animation_speed() / 1000
        self.orientation = (self.current_node_key, self.next_node_key)

        if (not self.is_loading or not self.is_dumping) and self.speed == 0:
            self.render.queue += timedelta
            self.render.score -= timedelta * 0.5
            self.render.reward -= timedelta * 0.5

        if self.current_node_key in self.render.load_spots or self.current_node_key in self.render.dump_spots:
            self.speed = 0.

        if self.current_node_key in self.render.load_spots and self.is_load is False and self.speed == 0 and self.current_node_key in self.render.shovels_dict:

            shovel = self.render.shovels_dict[self.current_node_key]
            if shovel.current_truck is None and shovel.is_loading is False:
                self.is_loading = True
                shovel.set_load_time(self.truck_id, self.payload)
            if shovel.current_truck == self.truck_id and shovel.is_loading is True:
                shovel.add_load_time(timedelta)
                self.current_load = shovel.current_load
                self.is_load = not shovel.is_loading
                self.is_loading = shovel.is_loading
                self.material_type = shovel.material_spot_type if self.is_load else None
            return

        if self.current_node_key in self.render.dump_spots and self.speed == 0 and self.is_load:
            dump = self.render.dumps_dict[self.current_node_key]
            if dump.type == 'crusher' and self.is_load:
                if dump.current_truck is None and dump.is_dumping is False:
                    dump.set_dump_time(self.truck_id, self.current_load)
                    self.is_dumping = True
                if dump.current_truck == self.truck_id and dump.is_dumping is True:
                    dump.add_dump_time(timedelta, self.material_type)
                    self.current_load = dump.current_load
                    if self.current_load == 0:
                        self.is_load = False
                    else:
                        self.is_load = True
                    if not self.is_load:
                        self.is_dumping = False
                        self.material_type = 'none'
                return

            if dump.type == 'dump_zone' and self.is_load:
                if self.truck_id not in dump.trucks_times.keys():
                    dump.set_dump_time(self.truck_id, self.current_load, self.material_type)
                    dump.add_dump_time(self.truck_id, timedelta)
                    self.is_dumping = True
                elif dump.trucks_times[self.truck_id][0] == 0:
                    dump.set_dump_time(self.truck_id, self.current_load, self.material_type)
                    dump.add_dump_time(self.truck_id, timedelta)
                    self.is_dumping = True
                elif dump.trucks_times[self.truck_id][0] != 0 and dump.trucks_times[self.truck_id][2]:
                    dump.add_dump_time(self.truck_id, timedelta)
                    self.is_load = dump.trucks_times[self.truck_id][2]
                    self.current_load = dump.trucks_times[self.truck_id][3]
                    if not self.is_load:
                        self.is_dumping = False
                        self.material_type = 'none'
                return

        if self.pos == self.to:

            for key in drawables.keys():
                if type(key) == tuple:
                    if (key[0] == self.current_node_key or key[1] == self.current_node_key) and (
                            key[0] == self.old_node_key or key[1] == self.old_node_key):
                        drawables[key].remove_from_queue(self.truck_id, self.orientation)

                if type(key) == str:
                    if drawables[key].get_coords() == self.pos:
                        if self.current_node_key in self.path and self.path.index(self.current_node_key) == 0:
                            self.path.remove(self.current_node_key)
                        self.old_node_key = copy(self.current_node_key)
                        self.current_node_key = key
                        if len(self.path) > 0:
                            self.next_node_key = self.path[0]
                            self.to = drawables[self.path.pop(0)].get_coords()

        self.update_segment_parameters(drawables)

        if (self.to - self.pos).magnitude() != 0:
            speed = self.speed
            if ((self.to - self.pos).normalize() * timedelta * speed).length() < (
                    self.pos - self.to).length():
                self.old_pos = copy(self.pos)
                self.pos = self.pos + (self.to - self.pos).normalize() * timedelta * speed
            else:
                self.old_pos = copy(self.pos)
                self.pos = self.to

            # direction = self.to-self.pos
            # old_direction = self.pos-self.old_pos
            #
            # if direction.length() != 0 and old_direction.length() != 0:
            #     rotation = Vector3(0,-180,0).angle_to(old_direction.normalize())
            #     if not math.isnan(rotation):
            #         print(rotation)
            #         self.image = pygame.transform.rotate(self.or_image, rotation)
            if self.is_load:
                if self.material_type == 'mineral':
                    self.image = self.or_mineral_load_image
                elif self.material_type == 'waste':
                    self.image = self.or_waste_load_image
            else:
                self.image = self.or_empty_image
            self.rect = self.image.get_rect(center=Vector2(self.pos.x, self.pos.y))

        self.text.update_in(self.pos, f'{self.truck_id} - {round(self.current_load)}')

    def move_to_node(self, to_node_key):
        if self.current_load > 0 and self.is_load and to_node_key in self.render.load_spots:
            return
        if not self.is_load and to_node_key in self.render.dump_spots:
            return
        self.path = self.render.find_path(self.next_node_key)[to_node_key]
        self.path.insert(0, self.next_node_key)

    def update_segment_parameters(self, drawables):
        if self.current_node_key != self.next_node_key:
            for key in drawables.keys():
                if type(key) == tuple:
                    if (key[0] == self.current_node_key or key[1] == self.current_node_key) and (
                            key[0] == self.next_node_key or key[1] == self.next_node_key):
                        self.update_speed(drawables[key])
                        drawables[key].update_queue(self.truck_id, self.speed, self.pos, self.orientation)

    def update_speed(self, segment: Segment):

        self.speed = segment.get_speeds()[0] * self.efficiency if self.is_load else \
            segment.get_speeds()[1] * self.efficiency
        dic = segment.get_dic(self.orientation)

        if dic is None:
            return
        if self.truck_id in dic.keys():
            truck_index = list(dic.keys()).index(self.truck_id)

            if (len(dic.keys()) > 1 and truck_index != 0 and list(dic.items())[truck_index - 1][1][0] < self.speed) or \
                    self.speed == 0:
                distance = (dic[self.truck_id][1] - list(dic.items())[truck_index - 1][1][1]).magnitude()
                if distance < 5:
                    self.speed = 0
                elif 9 > distance >= 5:
                    self.speed = list(dic.items())[truck_index - 1][1][0] / 2
                elif 15 >= distance >= 9:
                    self.speed = list(dic.items())[truck_index - 1][1][0]
                else:
                    self.speed = segment.get_speeds()[0] * self.efficiency if self.is_load \
                        else segment.get_speeds()[1] * self.efficiency

            if truck_index == 0:
                self.speed = segment.get_speeds()[0] * self.efficiency if self.is_load else \
                    segment.get_speeds()[1] * self.efficiency

    def get_id(self):
        return self.truck_id
