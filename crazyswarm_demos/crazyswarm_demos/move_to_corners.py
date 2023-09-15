#!/usr/bin/env python

import numpy as np
from crazyflie_py import *


XMIN = -6.5 + 0.5
XMAX = 7 - 0.5
YMIN = -3.5 + 0.5
YMAX = 3.5 - 0.5
Z = 2.8

def main():
    
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    allcfs.takeoff(targetHeight=Z, duration=1.0+Z)
    timeHelper.sleep(1.5+Z)


    for cf in allcfs.crazyflies:
        pos = [XMIN, YMAX, Z]
        cf.goTo(pos, 0., 8.0)
    timeHelper.sleep(8.0)


    for cf in allcfs.crazyflies:
        pos = [XMIN, YMIN, Z]
        cf.goTo(pos, 0., 8.0)
    timeHelper.sleep(8.0)
   
    for cf in allcfs.crazyflies:
        pos = [XMAX, YMIN, Z]
        cf.goTo(pos, 0., 15.0)
    timeHelper.sleep(15.0)
   
    for cf in allcfs.crazyflies:
        pos = [XMAX, YMAX, Z]
        cf.goTo(pos, 0., 8.0)
    timeHelper.sleep(8.0)
   
    # for cf in allcfs.crazyflies:
    #     pos = [-6, 2.75, Z]
    #     cf.goTo(pos, 0., 8.0)
    # timeHelper.sleep(8.0+Z)

    for cf in allcfs.crazyflies:
        pos = [0.0, 0.0, Z]
        cf.goTo(pos, 0., 8.0)
    timeHelper.sleep(8.0)

    allcfs.land(targetHeight=0.02, duration=1.0+Z)
    timeHelper.sleep(1.0+Z)

if __name__ == "__main__":
    main()
