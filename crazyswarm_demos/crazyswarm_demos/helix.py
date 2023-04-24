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

DURATION = 30.0
SPEED = np.abs(X_MAX - X_MIN) / DURATION

def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs
    
    if DIRECTION < 0:
        x_offset = X_MAX
    else:
        x_offset = X_MIN


    fx = lambda t: DIRECTION * t * SPEED + x_offset
    fy = lambda t: 0.5*np.sin(t)
    fz = lambda t: 0.5*np.cos(t) + 1.25

    period_offset = np.linspace(0, 2*np.pi, len(allcfs.crazyflies), endpoint=False)
    starting_positions = [(fx(0), fy(offset), fz(offset), 0) for offset in period_offset]

    allcfs.takeoff(targetHeight=1., duration=2.)
    timeHelper.sleep(4.0)

    for cf, pos in zip(allcfs.crazyflies, starting_positions):
        cf.goTo(pos, 0, 4.0)
        timeHelper.sleep(3.0)
    
    timeHelper.sleep(4.0)

    t = 0
    while t <= DURATION + 1.0:
        for cf, offset in zip(allcfs.crazyflies, period_offset):
            if t <= DURATION:
                pos = (fx(t), fy(t+offset), fz(t+offset))
            else:
                end_pos = (fx(DURATION), fy(DURATION+offset), fz(DURATION+offset))
                pos = end_pos
            cf.cmdPosition(pos)
        t += TIMESTEP
        timeHelper.sleepForRate(1/TIMESTEP)
    
    # Return to starting positions
    t = 0
    while t <= 7.5:
       for i, cf in enumerate(allcfs.crazyflies):
           if t <= i*0.75:
              pos = (fx(DURATION), fy(DURATION+period_offset[i]), fz(DURATION+period_offset[i]))
           else:
              end_pos = (fx(DURATION), fy(DURATION+period_offset[i]), fz(DURATION+period_offset[i]))
              init_pos = np.array(cf.initialPosition) + np.array([0, 0, 1.0 + i*0.5])
              pos = (1 - t/ 7.5) * np.array(end_pos) + (t / 7.5) * np.array(init_pos)
           cf.cmdPosition(pos)
       t += TIMESTEP
       timeHelper.sleepForRate(1/TIMESTEP)
    # Land
    t = 0
    while t <= 3.0:
        for i, cf in enumerate(allcfs.crazyflies):
            end_pos = np.array(cf.initialPosition) + np.array([0, 0, 1.0 + i*0.5])
            init_pos = np.array(cf.initialPosition)
            pos = (1-t/3.0) * end_pos + (t/3.0) * init_pos
            cf.cmdPosition(pos)
        t += TIMESTEP
        timeHelper.sleepForRate(1/TIMESTEP)
    print("Landed!")

if __name__ == "__main__":
    main()
