#!/usr/bin/env python

import numpy as np
from crazyflie_py import *


def main():
    Z = 1.8

    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    allcfs.takeoff(targetHeight=Z, duration=1.0 + Z)
    timeHelper.sleep(1.5 + Z)
    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
        cf.goTo(pos, 0.0, 5)

    timeHelper.sleep(5.5)

    allcfs.land(targetHeight=0.04, duration=1.0 + Z)
    timeHelper.sleep(1.5 + Z)


if __name__ == "__main__":
    main()
