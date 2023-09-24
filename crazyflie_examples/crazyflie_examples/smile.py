#!/usr/bin/env python

import numpy as np
from pathlib import Path

from crazyflie_py import *
from crazyflie_py.uav_trajectory import Trajectory

radius_big = 1.0
center_big = 1.25
Hz = 15
def fy1(t):
    t/=3
    return radius_big * np.sin(t)

def fx1(t):
    return 0.0

def fz1(t):
    t /= 3
    return -radius_big * np.cos(t) + center_big

def fy2(t):
    t /= 3
    t /= 2*np.pi / 1.9
    return np.sin(t + 1.4*np.pi/2)

def fz2(t):
    t /= 3
    t /= 2*np.pi / 1.9
    return np.cos(t + 1.4*np.pi/2) + center_big + 0.3

def fx2(t):
    return 0.5

eyes = ((-1.0, -0.5, 0.4+center_big), (-0.5, 0.5, 0.4+center_big))


def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs
    crazyflies = allcfs.crazyflies


    for cf in crazyflies:
        cf.setLEDColor(0, 0, 0)
        cf.takeoff(1.0, 2.0)
    timeHelper.sleep(2.5)

    crazyflies[0].goTo(eyes[0], 0., 3.0)
    crazyflies[1].goTo(eyes[1], 0., 3.0)
    crazyflies[2].goTo((fx1(0), fy1(0), fz1(0)), 0.0, 3.0)
    crazyflies[3].goTo((fx2(0), fy2(0), fz2(0)), 0.0, 3.0)

    timeHelper.sleep(3.5)
    for cf in crazyflies:
        cf.setLEDColor(255, 255, 0)
    timeHelper.sleep(0.5)

    timesteps = np.arange(0, 2*np.pi*3, 1/Hz)
    for t in timesteps:
        crazyflies[2].cmdPosition((fx1(t), fy1(t), fz1(t)), 0.0)
        crazyflies[3].cmdPosition((fx2(t), fy2(t), fz2(t)), 0.0)
        timeHelper.sleepForRate(Hz)
    
    crazyflies[2].notifySetpointsStop()
    crazyflies[3].notifySetpointsStop()
    t = timesteps[-1]
    crazyflies[2].goTo((fx1(t), fy1(t), fz1(t)), 0.0, 1.0)
    crazyflies[3].goTo((fx2(t), fy2(t), fz2(t)), 0.0, 1.0)
    for cf in crazyflies:
        cf.setLEDColor(0, 0, 0)
    timeHelper.sleep(1.0)
 
    for cf in crazyflies:
        pos = cf.initialPosition
        pos[2] += 1
        cf.goTo(pos, 0.0, 3.0)
    timeHelper.sleep(3.5)
    allcfs.land(0.04, 2.5)   


if __name__ == "__main__":
    main()
