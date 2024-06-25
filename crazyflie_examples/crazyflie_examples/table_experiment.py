#!/usr/bin/env python

import numpy as np
from crazyflie_py import *


def main():
    Z = 0.54

    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    allcfs.takeoff(targetHeight=Z, duration=1.0 + Z)
    timeHelper.sleep(1.5 + Z)
    # Move to start positions...
    for i, cf in enumerate(allcfs.crazyflies):
        if i == 0:
            rotation = np.pi / 4
        else:
            rotation = 0
        pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
        cf.goTo(pos, rotation, 5)
    timeHelper.sleep(5.5)

    # Cross the table...
    for i, cf in enumerate(allcfs.crazyflies):
        if i == 0:
            rotation = np.pi / 4
        else:
            rotation = 0
        pos = np.array(cf.initialPosition) + np.array([0, 2, Z])
        cf.goTo(pos, rotation, 10)
    timeHelper.sleep(10.5)

    # Cross the table...
    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
        cf.goTo(pos, 0.0, 10)

    timeHelper.sleep(10.5)

    allcfs.land(targetHeight=0.04, duration=1.0 + Z)
    timeHelper.sleep(1.5 + Z)


if __name__ == "__main__":
    main()
