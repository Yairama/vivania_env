from typing import Optional, Union, Tuple

import numpy as np
import matplotlib.pyplot as plt
import PIL.Image as Image
import gym
import random

import pygame
from gym import Env, spaces
import time

from gym.core import ObsType, ActType
from pygame.math import Vector3

from components.Node import Node
from components.Segment import Segment
from components.Shovel import Shovel
from components.Truck import Truck
from engine.RenderCore import RenderCore
from engine.utils.Dijkstra import Dijkstras


class VivaniaEnv(Env):

    def __init__(self):
        super(VivaniaEnv, self).__init__()
        # Define a 2-D observation space
        self.reward = 0.
        self.observation_shape = (1280, 720, 3)
        self.observation_space = spaces.Box(low=np.float32(np.zeros(self.observation_shape)),
                                            high=np.float32(np.ones(self.observation_shape)),
                                            dtype=np.float32)

        # Define an action space ranging from 0 to 4
        self.action_space = spaces.Discrete(6, )

        # Define elements present inside the environment
        self.elements = []
        self.render_core = None
        self.trucks_dict = dict

    def step(self, action: ActType) -> Tuple[ObsType, float, bool, dict]:
        pass

    def reset(self):
        nodes_dict = self.make_nodes()
        segments_dict = self.make_segments(nodes_dict)
        dijkstra = Dijkstras(nodes_dict)
        self.render_core = RenderCore('Vivania Core', dijkstra)
        self.render_core.add_drawables(nodes_dict)
        self.render_core.add_drawables(segments_dict)
        self.render_core.set_shovels(self.make_shovels(self.render_core))
        self.trucks_dict = self.make_trucks(self.render_core)

    def render(self, mode="human"):
        assert mode in ["human", "rgb_array"], "Invalid mode, must be either \"human\" or \"rgb_array\""
        if mode == "human":
            self.render_core.render()
        elif mode == "rgb_array":
            self.render_core.render()
            return self.render_core.get_pixel_image()

    def close(self):
        pygame.quit()
        self.render_core = None

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
        n_dump_zone = Node('dump_zone', Vector3(81, 256, 0), ['n5'])
        n_n6 = Node('n6', Vector3(521, 319, 0), ['n5', 'n7'])
        n_n7 = Node('n7', Vector3(569, 417, 0), ['n6', 'n8'])
        n_n8 = Node('n8', Vector3(593, 600, 0), ['n7', 'c2', 'n9'])
        n_c2 = Node('c2', Vector3(612, 751, 0), ['n8'])
        n_n9 = Node('n9', Vector3(446, 804, 0), ['n8', 'c3', 'n10'])
        n_c3 = Node('c3', Vector3(331, 846, 0), ['n9'])
        n_c3.material = 'mineral'
        n_n10 = Node('n10', Vector3(323, 801, 0), ['n9', 'n11'])
        n_n11 = Node('n11', Vector3(280, 689, 0), ['n12', 'n10'])
        n_n12 = Node('n12', Vector3(286, 537, 0), ['n11', 'n14', 'n13'])
        n_n13 = Node('n13', Vector3(305, 404, 0), ['n12', 'c4'])
        n_c4 = Node('c4', Vector3(426, 377, 0), ['n13'])
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
        for key in nodes_list.keys():
            start = nodes_list[key].get_coords()
            for sub_node_key in nodes_list[key].get_neighborhoods():
                end = nodes_list[sub_node_key].get_coords()
                if segments_list.get((key, sub_node_key)) is None and segments_list.get((sub_node_key, key)) is None:
                    segments_list[(key, sub_node_key)] = Segment(start, end, random.uniform(24., 30.),
                                                                 random.uniform(12., 18.))

        return segments_list

    def make_shovels(self, group):
        shovels_dict = {'c4': Shovel(group, 'Shovel c4', 'c4', 40, 0.9),
                        'c3': Shovel(group, 'Shovel c3', 'c3', 40, 0.9),
                        'c2': Shovel(group, 'Shovel c2', 'c2', 40, 0.9),
                        'c1': Shovel(group, 'Shovel c1', 'c1', 40, 0.9)}
        return shovels_dict

    def make_trucks(self, render):
        trucks_dict = {
            1: Truck(Vector3(91, 926, 0), render, 1, 0.65, 200),
            2: Truck(Vector3(91, 926, 0), render, 2, 0.75, 200),
            3: Truck(Vector3(91, 926, 0), render, 3, 0.9, 200),
            4: Truck(Vector3(91, 926, 0), render, 4, 0.89, 200),
            5: Truck(Vector3(91, 926, 0), render, 5, 0.79, 200),
            6: Truck(Vector3(91, 926, 0), render, 6, 0.81, 200),
            7: Truck(Vector3(91, 926, 0), render, 7, 0.77, 200),
            8: Truck(Vector3(91, 926, 0), render, 8, 0.85, 200),
            9: Truck(Vector3(91, 926, 0), render, 9, 0.70, 200),
            10: Truck(Vector3(91, 926, 0), render, 10, 0.84, 200),
            11: Truck(Vector3(91, 926, 0), render, 11, 0.95, 200),
            12: Truck(Vector3(91, 926, 0), render, 12, 0.99, 200),
            13: Truck(Vector3(91, 926, 0), render, 13, 0.76, 200),
            14: Truck(Vector3(91, 926, 0), render, 14, 0.83, 200),
        }
        return trucks_dict
