#!/usr/bin/env python

import numpy as np
from pathlib import Path

from crazyflie_py import *
from crazyflie_py.bezier_trajectory import BezierTrajectory


def main():

    print(
        "WARNING: running a script involving Bezier curves. Currently only cflib backend is supported. Please run the server with 'ros2 launch crazyflie launch.py backend:=cflib'."
    )

    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    traj = BezierTrajectory.from_json(
        Path(__file__).parent / "data/figure8_bezier.json"
    )

    TRIALS = 1
    TIMESCALE = 1.0
    for i in range(TRIALS):
        for cf in allcfs.crazyflies:
            cf.uploadBezierTrajectory(0, 0, trajectory=traj)
            cf.uploadBezierTrajectory(1, 0, trajectory=traj) # upload multiple trajectory is possible

        allcfs.takeoff(targetHeight=1.0, duration=2.0)
        timeHelper.sleep(2.5)
        for cf in allcfs.crazyflies:
            pos = np.array(cf.initialPosition) + np.array([0, 0, 1.0])
            cf.goTo(pos, 0, 4.0)
        timeHelper.sleep(4.5)

        allcfs.startTrajectory(0, timescale=TIMESCALE)
        timeHelper.sleep(traj.total_time * TIMESCALE + 2.0)
        # allcfs.startTrajectory(1, timescale=TIMESCALE)
        # timeHelper.sleep(traj.total_time * TIMESCALE + 2.0)

        timeHelper.sleep(4.5)
        allcfs.land(targetHeight=0.0, duration=2.0)
        timeHelper.sleep(3.0)


if __name__ == "__main__":
    main()
