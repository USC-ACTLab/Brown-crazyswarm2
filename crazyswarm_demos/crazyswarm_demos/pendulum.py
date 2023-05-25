#


from crazyflie_py import Crazyswarm
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import approximate_taylor_polynomial
from crazyflie_py.uav_trajectory import Trajectory
from crazyflie_py.generate_trajectory import *
from pathlib import Path

TAKEOFF_DURATION = 2.
HOVER_DURATION = 2.5
X_MIN = -8.0
X_MAX = 2.0
DIRECTION = -1
TIMESTEP = 1/100
RADIUS = 0.5
DURATION = 30.0
SPEED = np.abs(X_MAX - X_MIN) / DURATION
hz = 30

np.random.seed(42)

def get_lengths(N):
    g = 9.81
    n = 1
    Tmax = 60
    l = 1. #some initial guess value for the radius of the first drone

    k = 1/(2*3.14/Tmax * (l/g)**0.5) - n - 1

    ls = []

    for i in range(1, N + 1):
        ls.append(g * (Tmax / (2 * np.pi * (k + i + 1)))**2)
    return ls

def main():

    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    ls = get_lengths(len(allcfs.crazyflies))

    # Sort CFs by decreasing X coordinate, ties are broken with a random number 
    sorted_cfs = reversed(sorted([(cf.initialPosition[0], np.random.uniform(), cf) for cf in allcfs.crazyflies]))
    cfs = []
    for p, r, cf in sorted_cfs:
        cfs.append(cf)
    allcfs.crazyflies = cfs
    
    #Takeoff all drones
    allcfs.takeoff(1.0, 2.0)
    timeHelper.sleep(3.0)

    # Move to starting locations
    for i, cf in enumerate(allcfs.crazyflies):
        cf.goTo((2 - 0.5*i, 0., 1.5), 0, duration=5.0)
        timeHelper.sleep(1.0)
    timeHelper.sleep(5.0)

    # Pendulum Motion
    fy = lambda L, theta: L * np.sin(theta)
    f_theta = lambda L, t: np.pi / 4 * np.sin(np.sqrt(9.81 / L) * t)

    t = 0
    while t <= 60:
        for i, (l, cf) in enumerate(zip(ls, allcfs.crazyflies)):
            theta = f_theta(l, t)
            y = fy(l, theta)
            cf.cmdPosition((2 - 0.5*i, y, 1.5))
        timeHelper.sleepForRate(hz)
        t += 1/ hz
            

    # Land
    for cf in allcfs.crazyflies:
        cf.notifySetpointsStop()
        goal_position = cf.initialPosition + np.array([0., 0., 1.])
        cf.goTo(goal_position, 0., 5.0)
    timeHelper.sleep(5.0)
    allcfs.land(0.02, 2.0)

if __name__ == "__main__":
    main()
