# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pygame

from RenderCore import RenderCore
from Node import Node
from Truck import Truck
from RenderCore import RenderCore


def init():
    # Use a breakpoint in the code line below to debug your script.

    n_parking = Node('parking', 91, 926, 0, ['n2'])
    n_n1 = Node('n1', 223, 993, 0, ['crusher', 'n2'])
    n_crusher = Node('crusher', 314, 936, 0, ['n1'])
    n_n2 = Node('n2', 100, 823, 0, ['park', 'n1', 'n3'])
    n_n3 = Node('n3', 180, 682, 0, ['n2', 'n4'])
    n_n4 = Node('n4', 201, 457, 0, ['n3', 'n5'])
    n_n5 = Node('n5', 320, 302, 0, ['botadero', 'c1', 'n4', 'n6'])
    n_c1 = Node('c1', 548, 293, 0, ['n5'])
    n_dump_zone = Node('dump_zone', 81, 256, 0, ['n5'])
    n_n6 = Node('n6', 521, 319, 0, ['n5', 'n7'])
    n_n7 = Node('n7', 569, 417, 0, ['n6', 'n8'])
    n_n8 = Node('n8', 593, 600, 0, ['n7', 'c2', 'n9'])
    n_c2 = Node('c2', 612, 751, 0, ['n8'])
    n_n9 = Node('n9', 446, 804, 0, ['n8', 'c3', 'n10'])
    n_c3 = Node('c3', 331, 846, 0, ['n9'])
    n_n10 = Node('n10', 323, 801, 0, ['n9', 'n11'])
    n_n11 = Node('n11', 280, 689, 0, ['n12', 'n10'])
    n_n12 = Node('n12', 286, 537, 0, ['n11', 'n14', 'n13'])
    n_n13 = Node('n13', 305, 404, 0, ['n12', 'c4'])
    n_c4 = Node('c4', 426, 377, 0, ['n13'])
    n_n14 = Node('n14', 354, 440, 0, ['n12', 'n15'])
    n_n15 = Node('n15', 472, 473, 0, ['n14', 'n16'])
    n_n16 = Node('n16', 485, 549, 0, ['n15', 'c6', 'c5'])
    n_c5 = Node('c5', 413, 727, 0, ['n16'])
    n_c6 = Node('c6', 359, 618, 0, ['n16'])

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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    render = RenderCore()
    Truck((640, 360), render)
    nodes_list = init()
    render.add_drawables(nodes_list.values())
    render.render()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
