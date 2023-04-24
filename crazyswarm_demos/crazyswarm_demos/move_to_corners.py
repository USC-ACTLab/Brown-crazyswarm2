#!/usr/bin/env python

import numpy as np
from crazyflie_py import *


def main():
    Z = 1.0
    
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    allcfs.takeoff(targetHeight=Z, duration=1.0+Z)
    timeHelper.sleep(1.5+Z)


    for cf in allcfs.crazyflies:
        pos = [-5.25, 2.75, Z]
        cf.goTo(pos, 0., 8.0)
    timeHelper.sleep(8.0+Z)


    for cf in allcfs.crazyflies:
        pos = [-5.25, -3., Z]
        cf.goTo(pos, 0., 8.0)
    timeHelper.sleep(8.0+Z)
   
    for cf in allcfs.crazyflies:
        pos = [7.0, -3., Z]
        cf.goTo(pos, 0., 15.0)
    timeHelper.sleep(15.0+Z)
   
    for cf in allcfs.crazyflies:
        pos = [7.0, 2.75, Z]
        cf.goTo(pos, 0., 8.0)
    timeHelper.sleep(8.0+Z)
   
    for cf in allcfs.crazyflies:
        pos = [0.0, 0.0, Z]
        cf.goTo(pos, 0., 8.0)
    timeHelper.sleep(8.0+Z)

    allcfs.land(targetHeight=0.02, duration=1.0+Z)
    timeHelper.sleep(1.0+Z)

if __name__ == "__main__":
    main()
