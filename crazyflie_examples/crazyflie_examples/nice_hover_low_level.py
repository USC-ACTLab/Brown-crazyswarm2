"""Takeoff-hover-land for one CF. Useful to validate hardware config."""

# from pycrazyswarm import Crazyswarm
from crazyflie_py import Crazyswarm
import numpy as np
import copy

TAKEOFF_DURATION = 2.5
HOVER_DURATION = 5.0
Hz = 20
swarm = Crazyswarm()
timeHelper = swarm.timeHelper

def run_cvx_com(cf, start, goal, duration):
    timesteps = np.linspace(0, duration, int(Hz*duration))
    print("start, goal", start, goal)
    for t in timesteps:
        lam = t / duration
        pos = (1 - lam) * start + lam * goal
        print(pos)
        cf.cmdPosition(pos, 0.0)
        timeHelper.sleepForRate(Hz)

def takeoff(cf, height, duration):
    start_pos = cf.initialPosition
    goal_pos = copy.copy(start_pos)
    goal_pos[2] += 1

    run_cvx_com(cf, start_pos, goal_pos, duration)

def hover(cf, height, duration):
    start_pos = copy.copy(cf.initialPosition)
    start_pos[2] += height
    goal_pos = start_pos

    run_cvx_com(cf, start_pos, goal_pos, duration)

def land(cf, height, duration):
    start_pos = copy.copy(cf.initialPosition)
    print("-------", start_pos)
    start_pos[2] += height
    goal_pos = cf.initialPosition
    
    run_cvx_com(cf, start_pos, goal_pos, duration)


def main():
    cf = swarm.allcfs.crazyflies[0]

    takeoff(cf, 1.0, 3.0)
    hover(cf, 1.0, 5.0)
    land(cf, 1.0, 3.0)


if __name__ == "__main__":
    main()
