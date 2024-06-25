#


from crazyflie_py import Crazyswarm
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import approximate_taylor_polynomial
from crazyflie_py.uav_trajectory import Trajectory
from crazyflie_py.generate_trajectory import *
from pathlib import Path

TAKEOFF_DURATION = 2.0
HOVER_DURATION = 2.5
X_MIN = 0.25
X_MAX = 2.25
DIRECTION = 1
TIMESTEP = 1 / 10
RADIUS = 2.0
PERIOD = 60
DURATION = 60.0
SPEED = np.abs(X_MAX - X_MIN) / DURATION

np.random.seed(42)


def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs
    allcfs.crazyflies[0].setLEDColor(0, 0, 0)
    b = 0
    colors_of_rgb = (
        [255, 0, 0],
        [0, 255, 0],
        [0, 0, 255],
        [0, 255, 255],
        [255, 0, 255],
    )
    # for cf in allcfs.crazyflies:
    #     cf.setLEDColor(
    #         r=colors_of_rgb[b][0], g=colors_of_rgb[b][1], b=colors_of_rgb[b][2]
    #     )
    #     b = (b + 1) % len(allcfs.crazyflies)

    if DIRECTION < 0:
        x_offset = X_MAX
    else:
        x_offset = X_MIN

    # Helix moving from positive x to negative x
    # hypotrochoid(groupState, 8/8, 0.9, 2/8, 0.6)
    # R = 3
    # r = 2.8
    # d = 0.6
    # s = 0.75
    R = 2
    r = 0.25
    d = 0.25
    s = 2
    fz = lambda t: DIRECTION * t * SPEED + x_offset
    fy = lambda t: 1 * np.sin(t / 8) + 0.25 * np.sin(t * 2.5)
    fx = lambda t: 1 * np.cos(t / 8) + 0.25 * np.cos(t * 2.5)

    # Sort CFs by decreasing X coordinate, ties are broken with a random number
    sorted_cfs = reversed(
        sorted(
            [
                (cf.initialPosition[0], np.random.uniform(), cf)
                for cf in allcfs.crazyflies
            ]
        )
    )
    cfs = []
    for p, r, cf in sorted_cfs:
        cfs.append(cf)
    allcfs.crazyflies = cfs
    # hypotrochoid(groupState, 7.5, 4, 3, 0.035)
    # Evenly space crazyflies around the circle, if many crazyflies are used, an x offset might be necessary
    period_offset = np.linspace(0, PERIOD, len(allcfs.crazyflies), endpoint=False)
    starting_positions = [
        (fx(offset), fy(offset), fz(0), 0) for offset in period_offset
    ]

    allcfs.takeoff(targetHeight=1.0, duration=2.0)
    timeHelper.sleep(4.0)
    colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (125, 125, 0), (0, 125, 125)]
    # Send CFs one by one to the starting positions on the circle
    for cf, pos, c in zip(allcfs.crazyflies, starting_positions, colors):
        # line 56 ERROR "Crazyflie object has no attribute 'set LED'"
        # cf.setLED(*c)
        cf.goTo(pos, 0, 3.0)
        timeHelper.sleep(2.0)

    timeHelper.sleep(4.0)
    for cf in allcfs.crazyflies:
        cf.setLEDColor(255, 0, 0)

    t = 0
    while t <= DURATION + 1.0:
        for cf, offset in zip(allcfs.crazyflies, period_offset):
            if t <= DURATION:
                pos = (fx(t + offset), fy(t + offset), fz(t))
            else:
                end_pos = (fx(DURATION + offset), fy(DURATION), fz(DURATION + offset))
                pos = end_pos
            cf.cmdPosition(pos)
        t += TIMESTEP
        timeHelper.sleepForRate(1 / TIMESTEP)

    # Return to starting positions
    # t = 0
    # while t <= 7.5:
    #     for i, cf in enumerate(allcfs.crazyflies):
    #         if t <= i * 0.75:
    #             pos = (
    #                 fx(DURATION),
    #                 fy(DURATION + period_offset[i]),
    #                 fz(DURATION + period_offset[i]),
    #             )
    #         else:
    #             end_pos = (
    #                 fx(DURATION),
    #                 fy(DURATION + period_offset[i]),
    #                 fz(DURATION + period_offset[i]),
    #             )
    #             init_pos = np.array(cf.initialPosition) + np.array([0, 0, 1.0])
    #             pos = (1 - t / 7.5) * np.array(end_pos) + (t / 7.5) * np.array(init_pos)
    #         cf.cmdPosition(pos)
    #     t += TIMESTEP
    #     timeHelper.sleepForRate(1 / TIMESTEP)
    # Land
    for cf in allcfs.crazyflies:
        cf.notifySetpointsStop()
        cf.setLEDColor(0, 0, 0)
        cf.land(0.04, 2.5)
    print("Landed!")


if __name__ == "__main__":
    main()
