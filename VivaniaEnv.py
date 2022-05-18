from typing import Optional, Union, Tuple
import os, sys

sys.path.insert(0, 'vivania_env')
import numpy as np
import matplotlib.pyplot as plt
import PIL.Image as Image
import gym
import random

import pygame
from gym import Env, spaces
import time

from pygame.math import Vector3

from components.Crusher import Crusher
from components.Dump import Dump
from components.Node import Node
from components.Segment import Segment
from components.Shovel import Shovel
from components.Truck import Truck
from engine.RenderCore import RenderCore
from engine.utils.Dijkstra import Dijkstras


class VivaniaEnv(Env):

    def __init__(self, hidden):
        super(VivaniaEnv, self).__init__()
        print("************** Created Vivavia's Environment **************")
        print(f"Hiding screen: {hidden}")
        # Define a 2-D observation space
        self.reward = 0.
        self.info = []
        self.amount_of_trucks = 25
        """
        Obs orden definition
        for n trucks should be:
        np.tile([is_loading, is_dumping, speed, material_type, tonnage, current_shovel],(n,1))
        """
        self.observation_space = spaces.Box(low=np.float32(np.tile([0, 0, 0, 0, 0, 0], (self.amount_of_trucks, 1))),
                                            high=np.float32(np.tile([1, 1, 30, 3, 350, 8], (self.amount_of_trucks, 1))),
                                            dtype=np.float32)
        self.action_space = spaces.MultiDiscrete(np.array([8] * self.amount_of_trucks))
        self.hidden = hidden
        # Define an action space ranging from 0 to 8
        self._max_episode_steps = 1000
        self.current_step = 0
        # Define elements present inside the environment
        self.elements = []
        self.render_core: RenderCore = None
        self.trucks_list = list
        self.nodes_to = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'crusher', 'dump_zone']

        self.score = 0.

    def step(self, action):
        self.render(mode="human")
        done = False
        self.current_step += 1
        assert self.action_space.contains(action), "Invalid Action"
        obs = []
        for i in range(len(action)):
            act = action[i]
            truck = self.trucks_list[i]


            truck.move_to_node(self.nodes_to[act])

            is_loading = int(truck.is_loading)
            is_dumping = int(truck.is_dumping)
            speed = truck.speed
            material_type = truck.material_type
            if material_type == 'mineral':
                material_type = 0
            elif material_type == 'waste':
                material_type = 1
            else:
                material_type = 2
            tonnage = truck.current_load
            current_node = truck.current_node_key

            if current_node == 'c1':
                current_node = 0
            elif current_node == 'c2':
                current_node = 1
            elif current_node == 'c3':
                current_node = 2
            elif current_node == 'c4':
                current_node = 3
            elif current_node == 'c5':
                current_node = 4
            elif current_node == 'c6':
                current_node = 5
            elif current_node == 'crusher':
                current_node = 6
            elif current_node == 'dump_zone':
                current_node = 7
            else:
                current_node = 8

            obs.append([is_loading, is_dumping, speed, material_type, tonnage, current_node])
            # truck.move_to_node('c1')

        # for act in action:
        #     for truck in trucks:
        #         if act == 8:
        #             continue
        #         else:
        #             truck.move_to_node(self.nodes_to[act])
        #             if truck.get_id() == 1:
        #                 print(truck.pos)
        #                 print(truck.path)
        self.reward = self.render_core.reward
        # self.render_core.reward -= 0.00001

        # self.render_core.score -= 0.00001
        self.score = self.render_core.score

        # if self.score <= -1000.:
        #     done = True

        if self.current_step > self._max_episode_steps:
            done = True
        obs = np.array(obs)

        return obs, self.reward, done, {}

    def reset(self):
        self.current_step = 0
        self.reward = 0.
        self.info = []
        pygame.quit()
        nodes_dict = self.make_nodes()
        segments_dict = self.make_segments(nodes_dict)
        dijkstra = Dijkstras(nodes_dict)
        self.render_core = RenderCore('Vivania Core', dijkstra, self.hidden)
        self.render_core.add_drawables(nodes_dict)
        self.render_core.add_drawables(segments_dict)
        self.render_core.set_shovels(self.make_shovels(self.render_core))
        self.render_core.set_dumps(self.make_dumps(self.render_core))
        self.render_core.load_spots = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6']
        self.render_core.dump_spots = ['dump_zone', 'crusher']
        self.trucks_list = self.make_trucks(self.render_core)

        return np.tile([0, 0, 0, 0, 0, 8], (self.amount_of_trucks, 1))

    def render(self, mode="human"):
        assert mode in ["human", "rgb_array"], "Invalid mode, must be either \"human\" or \"rgb_array\""
        if mode == "human":
            self.render_core.render()
            return self.render_core.get_pixel_image()
        elif mode == "rgb_array":
            self.render_core.render()
            return self.render_core.get_pixel_image()

    def make_nodes(self):
        # Use a breakpoint in the code line below to debug your script.

        n_parking = Node('parking', Vector3(91, 926, 0), ['n2'])
        n_n1 = Node('n1', Vector3(223, 993, 0), ['crusher', 'n2'])
        n_crusher = Node('crusher', Vector3(314, 936, 0), ['n1'])
        n_n2 = Node('n2', Vector3(100, 823, 0), ['parking', 'n1', 'n3'])
        n_n3 = Node('n3', Vector3(180, 682, 0), ['n2', 'n4'])
        n_n4 = Node('n4', Vector3(201, 457, 0), ['n3', 'n5'])
        n_n5 = Node('n5', Vector3(320, 302, 0), ['dump_zone', 'c1', 'n4', 'n6'])
        n_c1 = Node('c1', Vector3(548, 293, 0), ['n5'])
        n_c1.material = 'waste'
        n_dump_zone = Node('dump_zone', Vector3(81, 256, 0), ['n5'])
        n_n6 = Node('n6', Vector3(521, 319, 0), ['n5', 'n7'])
        n_n7 = Node('n7', Vector3(569, 417, 0), ['n6', 'n8'])
        n_n8 = Node('n8', Vector3(593, 600, 0), ['n7', 'c2', 'n9'])
        n_c2 = Node('c2', Vector3(612, 751, 0), ['n8'])
        n_c2.material = 'waste'
        n_n9 = Node('n9', Vector3(446, 804, 0), ['n8', 'c3', 'n10'])
        n_c3 = Node('c3', Vector3(331, 846, 0), ['n9'])
        n_c3.material = 'waste'
        n_n10 = Node('n10', Vector3(323, 801, 0), ['n9', 'n11'])
        n_n11 = Node('n11', Vector3(280, 689, 0), ['n12', 'n10'])
        n_n12 = Node('n12', Vector3(286, 537, 0), ['n11', 'n14', 'n13'])
        n_n13 = Node('n13', Vector3(305, 404, 0), ['n12', 'c4'])
        n_c4 = Node('c4', Vector3(426, 377, 0), ['n13'])
        n_c4.material = 'waste'
        n_n14 = Node('n14', Vector3(354, 440, 0), ['n12', 'n15'])
        n_n15 = Node('n15', Vector3(472, 473, 0), ['n14', 'n16'])
        n_n16 = Node('n16', Vector3(485, 549, 0), ['n15', 'c6', 'c5'])
        n_c5 = Node('c5', Vector3(413, 727, 0), ['n16'])
        n_c5.material = 'mineral'
        n_c6 = Node('c6', Vector3(359, 618, 0), ['n16'])
        n_c6.material = 'mineral'

        return {n_parking.name: n_parking,
                n_n1.name: n_n1,
                n_crusher.name: n_crusher,
                n_n2.name: n_n2,
                n_n3.name: n_n3,
                n_n4.name: n_n4,
                n_n5.name: n_n5,
                n_c1.name: n_c1,
                n_dump_zone.name: n_dump_zone,
                n_n6.name: n_n6,
                n_n7.name: n_n7,
                n_n8.name: n_n8,
                n_c2.name: n_c2,
                n_n9.name: n_n9,
                n_c3.name: n_c3,
                n_n10.name: n_n10,
                n_n11.name: n_n11,
                n_n12.name: n_n12,
                n_n13.name: n_n13,
                n_c4.name: n_c4,
                n_n14.name: n_n14,
                n_n15.name: n_n15,
                n_n16.name: n_n16,
                n_c5.name: n_c5,
                n_c6.name: n_c6}

    def make_segments(self, nodes_list: dict):
        segments_list = {}
        # for key in nodes_list.keys():
        #     start = nodes_list[key].get_coords()
        #     for sub_node_key in nodes_list[key].get_neighborhoods():
        #         end = nodes_list[sub_node_key].get_coords()
        #         if segments_list.get((key, sub_node_key)) is None and segments_list.get((sub_node_key, key)) is None:
        #             segments_list[(key, sub_node_key)] = Segment(start, end, random.uniform(24., 30.),
        #                                                          random.uniform(12., 18.))
        segments_list[('parking', 'n2')] = Segment(nodes_list['parking'].get_coords(), nodes_list['n2'].get_coords(),
                                                   random.uniform(24., 30.), random.uniform(12., 18.),
                                                   ('parking', 'n2'))
        segments_list[('crusher', 'n1')] = Segment(nodes_list['crusher'].get_coords(), nodes_list['n1'].get_coords(),
                                                   random.uniform(24., 30.), random.uniform(12., 18.),
                                                   ('crusher', 'n1'))
        segments_list[('n1', 'n2')] = Segment(nodes_list['n1'].get_coords(), nodes_list['n2'].get_coords(),
                                              random.uniform(24., 30.), random.uniform(12., 18.), ('n1', 'n2'))
        segments_list[('n2', 'n3')] = Segment(nodes_list['n2'].get_coords(), nodes_list['n3'].get_coords(),
                                              random.uniform(24., 30.), random.uniform(12., 18.), ('n2', 'n3'))
        segments_list[('n3', 'n4')] = Segment(nodes_list['n3'].get_coords(), nodes_list['n4'].get_coords(),
                                              random.uniform(24., 30.), random.uniform(12., 18.), ('n3', 'n4'))
        segments_list[('n4', 'n5')] = Segment(nodes_list['n4'].get_coords(), nodes_list['n5'].get_coords(),
                                              random.uniform(24., 30.), random.uniform(12., 18.), ('n4', 'n5'))
        segments_list[('n5', 'n6')] = Segment(nodes_list['n5'].get_coords(), nodes_list['n6'].get_coords(),
                                              random.uniform(24., 30.), random.uniform(12., 18.), ('n5', 'n6'))
        segments_list[('n5', 'c1')] = Segment(nodes_list['n5'].get_coords(), nodes_list['c1'].get_coords(),
                                              random.uniform(24., 30.), random.uniform(12., 18.), ('n5', 'c1'))
        segments_list[('n5', 'dump_zone')] = Segment(nodes_list['n5'].get_coords(),
                                                     nodes_list['dump_zone'].get_coords(),
                                                     random.uniform(24., 30.), random.uniform(12., 18.),
                                                     ('n5', 'dump_zone'))
        segments_list[('n6', 'n7')] = Segment(nodes_list['n6'].get_coords(), nodes_list['n7'].get_coords(),
                                              random.uniform(24., 30.), random.uniform(12., 18.), ('n6', 'n7'))
        segments_list[('n7', 'n8')] = Segment(nodes_list['n7'].get_coords(), nodes_list['n8'].get_coords(),
                                              random.uniform(24., 30.), random.uniform(12., 18.), ('n7', 'n8'))
        segments_list[('n8', 'n9')] = Segment(nodes_list['n8'].get_coords(), nodes_list['n9'].get_coords(),
                                              random.uniform(24., 30.), random.uniform(12., 18.), ('n8', 'n9'))
        segments_list[('n8', 'c2')] = Segment(nodes_list['n8'].get_coords(), nodes_list['c2'].get_coords(),
                                              random.uniform(24., 30.), random.uniform(12., 18.), ('n8', 'c2'))
        segments_list[('n9', 'n10')] = Segment(nodes_list['n9'].get_coords(), nodes_list['n10'].get_coords(),
                                               random.uniform(24., 30.), random.uniform(12., 18.), ('n9', 'n10'))
        segments_list[('n9', 'c3')] = Segment(nodes_list['n9'].get_coords(), nodes_list['c3'].get_coords(),
                                              random.uniform(24., 30.), random.uniform(12., 18.), ('n9', 'c3'))
        segments_list[('n10', 'n11')] = Segment(nodes_list['n10'].get_coords(), nodes_list['n11'].get_coords(),
                                                random.uniform(24., 30.), random.uniform(12., 18.), ('n10', 'n11'))
        segments_list[('n11', 'n12')] = Segment(nodes_list['n11'].get_coords(), nodes_list['n12'].get_coords(),
                                                random.uniform(24., 30.), random.uniform(12., 18.), ('n11', 'n12'))
        segments_list[('n12', 'n13')] = Segment(nodes_list['n12'].get_coords(), nodes_list['n13'].get_coords(),
                                                random.uniform(24., 30.), random.uniform(12., 18.), ('n12', 'n13'))
        segments_list[('n12', 'n14')] = Segment(nodes_list['n12'].get_coords(), nodes_list['n14'].get_coords(),
                                                random.uniform(24., 30.), random.uniform(12., 18.), ('n12', 'n14'))
        segments_list[('n13', 'c4')] = Segment(nodes_list['n13'].get_coords(), nodes_list['c4'].get_coords(),
                                               random.uniform(24., 30.), random.uniform(12., 18.), ('n13', 'c4'))
        segments_list[('n14', 'n15')] = Segment(nodes_list['n14'].get_coords(), nodes_list['n15'].get_coords(),
                                                random.uniform(24., 30.), random.uniform(12., 18.), ('n14', 'n15'))
        segments_list[('n15', 'n16')] = Segment(nodes_list['n15'].get_coords(), nodes_list['n16'].get_coords(),
                                                random.uniform(24., 30.), random.uniform(12., 18.), ('n15', 'n16'))
        segments_list[('n16', 'c5')] = Segment(nodes_list['n16'].get_coords(), nodes_list['c5'].get_coords(),
                                               random.uniform(24., 30.), random.uniform(12., 18.), ('n16', 'c5'))
        segments_list[('n16', 'c6')] = Segment(nodes_list['n16'].get_coords(), nodes_list['c6'].get_coords(),
                                               random.uniform(24., 30.), random.uniform(12., 18.), ('n16', 'c6'))

        return segments_list

    def make_shovels(self, group):
        shovels_dict = {'c6': Shovel(group, 'Shovel c6', 'c6', 47, 0.91),
                        'c5': Shovel(group, 'Shovel c5', 'c5', 47, 0.92),
                        'c4': Shovel(group, 'Shovel c4', 'c4', 45, 0.89),
                        'c3': Shovel(group, 'Shovel c3', 'c3', 40, 0.82),
                        'c2': Shovel(group, 'Shovel c2', 'c2', 37, 0.80),
                        'c1': Shovel(group, 'Shovel c1', 'c1', 35, 0.7)}
        return shovels_dict

    def make_dumps(self, group):
        dumps_dict = {'crusher': Crusher(group, 'Crusher', 'crusher'),
                      'dump_zone': Dump(group, 'Dump', 'dump_zone')
                      }
        return dumps_dict

    def make_trucks(self, render):
        trucks_dict = {
            1: Truck(Vector3(91, 926, 0), render, 1, 0.68, 200),
            2: Truck(Vector3(91, 926, 0), render, 2, 0.75, 200),
            3: Truck(Vector3(91, 926, 0), render, 3, 0.9, 200),
            4: Truck(Vector3(91, 926, 0), render, 4, 0.89, 250),
            5: Truck(Vector3(91, 926, 0), render, 5, 0.79, 200),
            6: Truck(Vector3(91, 926, 0), render, 6, 0.81, 200),
            7: Truck(Vector3(91, 926, 0), render, 7, 0.77, 200),
            8: Truck(Vector3(91, 926, 0), render, 8, 0.85, 200),
            9: Truck(Vector3(91, 926, 0), render, 9, 0.70, 200),
            10: Truck(Vector3(91, 926, 0), render, 10, 0.84, 190),
            11: Truck(Vector3(91, 926, 0), render, 11, 0.95, 190),
            12: Truck(Vector3(91, 926, 0), render, 12, 0.99, 250),
            13: Truck(Vector3(91, 926, 0), render, 13, 0.76, 190),
            14: Truck(Vector3(91, 926, 0), render, 14, 0.83, 200),
            15: Truck(Vector3(91, 926, 0), render, 15, 0.84, 200),
            16: Truck(Vector3(91, 926, 0), render, 16, 0.95, 250),
            17: Truck(Vector3(91, 926, 0), render, 17, 0.99, 250),
            18: Truck(Vector3(91, 926, 0), render, 18, 0.76, 200),
            19: Truck(Vector3(91, 926, 0), render, 19, 0.83, 200),
            20: Truck(Vector3(91, 926, 0), render, 20, 0.89, 200),
            21: Truck(Vector3(91, 926, 0), render, 21, 0.79, 190),
            22: Truck(Vector3(91, 926, 0), render, 22, 0.81, 190),
            23: Truck(Vector3(91, 926, 0), render, 23, 0.77, 220),
            24: Truck(Vector3(91, 926, 0), render, 24, 0.85, 220),
            25: Truck(Vector3(91, 926, 0), render, 25, 0.88, 220)
        }
        return list(trucks_dict.values())

    # def close(self):
    #     self.render_core.quit()
    @property
    def max_episode_steps(self):
        return self._max_episode_steps
