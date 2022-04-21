from copy import copy

from numpy import Inf
import heapq


class Dijkstras:

    def __init__(self, nodes_dict: dict):
        self.graph = {}

        for key in nodes_dict.keys():
            connections_dict = []

            for secondary_key in nodes_dict[key].get_neighborhoods():
                node_tuple = \
                    (secondary_key, (nodes_dict[secondary_key].get_coords() - nodes_dict[key].get_coords()).magnitude())
                connections_dict.append(node_tuple)

            self.graph[key] = connections_dict

    def get_graph(self):
        return self.graph

    # TODO: Implement lazy_dijkstras

    # takes the graph and the starting node
    # returns a list of distances from the starting node to every other node
    def naive_dijkstras(self, root):
        graph = self.graph
        n = len(graph)

        keys = list(graph.keys())
        dist = {}
        visited = {}
        path = {}

        for key in keys:
            # initialize distance list as all infinities
            dist[key] = Inf
            # initialize list of visited nodes
            visited[key] = False
            path[key] = []
        # set the distance for the root to be 0
        dist[root] = 0

        # loop through all the nodes
        for _ in range(n):
            # "start" our node as -1 (so we don't have a start node yet)
            u = -1
            # loop through all the nodes to check for visitation status
            for i in range(n):
                # if the node 'i' hasn't been visited and
                # we haven't processed it or the distance we have for it is less
                # than the distance we have to the "start" node
                if not visited[keys[i]] and (u == -1 or dist[keys[i]] < dist[keys[u]]):
                    u = i
            # all the nodes have been visited or we can't reach this node
            if dist[keys[u]] == Inf:
                break
            # set the node as visited
            visited[keys[u]] = True
            # compare the distance to each node from the "start" node
            # to the distance we currently have on file for it
            for v, l in graph[keys[u]]:
                if dist[keys[u]] + l < dist[v]:
                    dist[v] = dist[keys[u]] + l
                    t_path = copy(path[keys[u]])
                    t_path.append(v)
                    path[v] = t_path

        return dist, path
