from copy import copy

import pygame, sys
from pygame.math import Vector2, Vector3

from components.Crusher import Crusher
from components.Segment import Segment
from components.Text import Text


class Truck(pygame.sprite.Sprite):
    def __init__(self, pos: Vector3, group, truck_id: int, efficiency: float, payload=200):
        """

        :rtype: object
        """
        super().__init__(group)
        self.image = pygame.image.load('resources/truck.png').convert_alpha()
        # self.image = pygame.transform.scale(self.image, (30 + (truck_id * truck_id), 20 + (truck_id * truck_id)))
        self.image = pygame.transform.scale(self.image, (30, 20))
        self.pos = pos
        self.to = pos
        self.truck_id = truck_id
        self.target_node = 'n1'
        self.old_pos = self.pos
        self.rect = self.image.get_rect(center=Vector2(self.pos.x, self.pos.y))
        self.direction = None
        self.speed = 25
        self.payload = payload
        self.is_load = False
        self.efficiency = efficiency

        self.render = group
        self.current_node_key = 'parking'
        self.next_node_key = 'parking'
        self.old_node_key = 'parking'
        self.current_segment_key = ('parking', 'parking')
        self.path = []
        self.current_load = 0
        self.text = Text(self.render, f'{self.truck_id} - {self.current_load}', 10, '#831010', 40, 12, self.pos)
        self.material_type = None
        self.counter = 0

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
            # self.direction.y = 1
        else:
            self.counter = 0

        # if keys[pygame.K_RIGHT]:
        #     pass
        # elif keys[pygame.K_LEFT]:
        #     pass
        # else:
        #     self.counter = 0

    def update(self):
        #self.input()

        drawables = self.render.drawables
        timedelta = self.render.get_animation_speed() / 1000
        self.direction = (self.current_node_key, self.next_node_key)

        if self.current_node_key in self.render.load_spots or self.current_node_key in self.render.dump_spots:
            self.speed = 0.

        if self.current_node_key in self.render.load_spots and self.is_load is False and self.speed == 0:
            shovel = self.render.shovels_dict[self.current_node_key]
            if shovel.current_truck is None and shovel.is_loading is False:
                shovel.set_load_time(self.truck_id, self.payload)
            if shovel.current_truck == self.truck_id and shovel.is_loading is True:
                shovel.add_load_time(timedelta)
                self.current_load = shovel.current_load
                self.is_load = not shovel.is_loading
                self.material_type = shovel.material_spot_type if self.is_load else None
            return

        if self.current_node_key in self.render.dump_spots and self.speed == 0 and self.is_load:
            dump = self.render.dumps_dict[self.current_node_key]
            if dump.type == 'crusher':
                dump: Crusher = self.render.dumps_dict[self.current_node_key]
                if dump.current_truck is None and dump.is_dumping is False:
                    dump.set_dump_time(self.truck_id, self.current_load)
                if dump.current_truck == self.truck_id and dump.is_dumping is True:
                    dump.add_dump_time(timedelta)
                    self.current_load = dump.current_load
                    self.is_load = not dump.is_dumping
                return

        # if self.is_load:
        #     if self.material_type == 'mineral':
        #         self.move_to_node('crusher')
        #     elif self.material_type == 'waste':
        #         self.move_to_node('dump_zone')


        # self.update_next_position(drawables)
        if self.pos == self.to:
            for key in drawables.keys():
                if type(key) == tuple:
                    if (key[0] == self.current_node_key or key[1] == self.current_node_key) and (
                            key[0] == self.old_node_key or key[1] == self.old_node_key):
                        drawables[key].remove_from_queue(self.truck_id, self.direction)

                if type(key) == str:
                    if drawables[key].get_coords() == self.pos:
                        if self.current_node_key in self.path and self.path.index(self.current_node_key)==0:
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
                self.rect = self.image.get_rect(center=Vector2(self.pos.x, self.pos.y))
            else:
                self.old_pos = copy(self.pos)
                self.pos = self.to
                self.rect = self.image.get_rect(center=Vector2(self.pos.x, self.pos.y))

        self.text.update_in(self.pos, f'{self.truck_id} - {round(self.current_load)}')
    #    def update_next_position(self, drawables):

    def move_to_node(self, to_node_key):
        # if self.truck_id == 1:
        #     print(self.render.find_path(self.next_node_key))
        #     print(self.old_node_key, self.current_node_key, self.next_node_key)
        self.path = self.render.find_path(self.next_node_key)[to_node_key]
        self.path.insert(0, self.next_node_key)
        # if self.truck_id == 1:
        #     print(self.path)
        #     print(self.old_node_key, self.current_node_key, self.next_node_key)
        # if len(self.path) > 0:
        #     self.old_node_key = self.current_node_key
        #     self.current_node_key = self.next_node_key
        #     self.next_node_key = self.path[0]

    def update_segment_parameters(self, drawables):
        if self.current_node_key != self.next_node_key:
            for key in drawables.keys():
                if type(key) == tuple:
                    if (key[0] == self.current_node_key or key[1] == self.current_node_key) and (
                            key[0] == self.next_node_key or key[1] == self.next_node_key):
                        self.update_speed(drawables[key])
                        drawables[key].update_queue(self.truck_id, self.speed, self.pos, self.direction)

    def update_speed(self, segment: Segment):

        self.speed = segment.get_speeds()[0] * self.efficiency if self.is_load else \
            segment.get_speeds()[1] * self.efficiency
        dic = segment.get_dic(self.direction)

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
