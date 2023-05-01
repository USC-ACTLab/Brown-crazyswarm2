from crazyflie_py import Crazyswarm
import numpy as np
from crazyflie_py.uav_trajectory import Trajectory
from crazyflie_py.generate_trajectory import *
import os


def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs
    n_testing = 29
    crazyflies = allcfs.crazyflies[:n_testing]
    for i in range(100):
        for cf in crazyflies:
            if i % 3 == 0:
                cf.setLEDColor(1, 0, 0)
            elif i % 3 == 1:
                cf.setLEDColor(0, 1, 0)
            else:
                cf.setLEDColor(0, 0, 1)
        timeHelper.sleep(3.0)

if __name__ == "__main__":
    main()
