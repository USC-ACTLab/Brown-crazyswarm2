#!/usr/bin/env python

import numpy as np
from pathlib import Path

from crazyflie_py import *


class BezierTrajectoryPiece:
    def __init__(self, bezier_curve):
        control_points = np.array(bezier_curve["control_points"])

        self.duration = bezier_curve["parameters"][0]
        self.x = control_points[:, 0]
        self.y = control_points[:, 1]
        self.z = control_points[:, 2]
        self.yaw = np.zeros_like(self.x)  # assume zero yaw for now


def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    # TODO: construct the trajectory
    bezier_curve = {
        "control_points": [
            [0.0, -1.0, 1.0],
            [0.0, -0.9999999999999999, 0.9999999999999999],
            [-0.07534305719147254, -0.9943341183411414, 1.000090823889544],
            [-0.19988495750934981, -0.9776819294183798, 1.0002323866263076],
            [-0.347480864044028, -0.9447239205531746, 1.0003846034356692],
            [-0.49199621358744006, -0.890133312602044, 1.0005073942908271],
            [-0.6072947829139111, -0.8085840281358084, 1.0005606778422909],
        ],
        "parameters": [5.0],
    }
    # Construct the bezier trajectory, ideally this should be done within uploadBezierTrajectory
    traj = BezierTrajectoryPiece(bezier_curve)
    traj = [traj]

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
        timeHelper.sleep(traj.duration * TIMESCALE + 2.0)

        timeHelper.sleep(4.5)
        allcfs.land(targetHeight=0.0, duration=2.0)
        timeHelper.sleep(3.0)


if __name__ == "__main__":
    main()
