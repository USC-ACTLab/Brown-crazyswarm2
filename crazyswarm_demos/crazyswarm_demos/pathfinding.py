
from crazyflie_py import Crazyswarm
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import approximate_taylor_polynomial
from crazyflie_py.uav_trajectory import Trajectory
from crazyflie_py.generate_trajectory import *
import networkx as nx

def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    cf = allcfs.crazyflies[0]

    start = (-1, -2)
    goal = (3, 3)

    path = findPath(start, goal)

    cf.takeoff(1.0, 3.0)
    timeHelper.sleep(3)

    cf.goTo((path[0][0], path[0][1], 1), 0, 3)
    timeHelper.sleep(3)

    for node in path:
        x = node[0]
        y = node[1]
        z = 1
        cf.goTo((x, y, z), 0, 1)
        timeHelper.sleep(1)
    
    cf.land(0.0, 3.0)

def findPath(start, goal):
    G = nx.grid_2d_graph(13, 13)
    # A = nx.nx_agraph.to_agraph(G)
    # A.draw("10x10.png", prog="neato")

    # print(list(G.nodes))
    # print(G.number_of_nodes())
    # print(G.number_of_edges())
    x1 = (start[0] * 2) + 6 
    y1 = (start[1] * 2) + 6
    x2 = (goal[0] * 2) + 6
    y2 = (goal[1] * 2) + 6

    def dist(a, b):
        (x1, y1) = a
        (x2, y2) = b
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    path = nx.astar_path(G, (x1, y1), (x2, y2), heuristic=dist, weight="cost") 
    newPath = []
    for node in path:
        newPath.append(((node[0] / 2) - 3 , (node[1] / 2) - 3))
    length = nx.astar_path_length(G, (0, 0), (2, 2), heuristic=dist, weight="cost")
    print("Path: ", newPath)
    print("Path length: ", length)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color="#f86e00")
    edge_labels = nx.get_edge_attributes(G, "cost")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()

    return newPath

if __name__ == '__main__':
    main()