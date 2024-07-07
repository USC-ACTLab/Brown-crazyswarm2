#!/usr/bin/env python

import numpy as np
from pathlib import Path

from crazyflie_py import *


def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    traj = BezierTrajectory()
    traj.from_json(Path(__file__).parent / "data/figure8_bezier.json")

    TRIALS = 1
    TIMESCALE = 1.0
    for i in range(TRIALS):
        for cf in allcfs.crazyflies:
            cf.uploadBezierTrajectory(0, 0, trajectory=traj)

        allcfs.takeoff(targetHeight=1.0, duration=2.0)
        timeHelper.sleep(2.5)
        for cf in allcfs.crazyflies:
            pos = np.array(cf.initialPosition) + np.array([0, 0, 1.0])
            cf.goTo(pos, 0, 4.0)
        timeHelper.sleep(4.5)

        allcfs.startTrajectory(0, timescale=TIMESCALE)
        timeHelper.sleep(traj.total_time * TIMESCALE + 2.0)

        timeHelper.sleep(4.5)
        allcfs.land(targetHeight=0.0, duration=2.0)
        timeHelper.sleep(3.0)


if __name__ == "__main__":
    main()
