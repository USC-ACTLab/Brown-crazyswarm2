"""Takeoff-hover-land for one CF. Useful to validate hardware config."""

# from pycrazyswarm import Crazyswarm
from crazyflie_py import Crazyswarm
import pickle
import numpy as np

TAKEOFF_DURATION = 5.5
HOVER_DURATION = 5.0

from conflicts import CBS


def main():
    paths = CBS(
        [(4, 0), (3, 0), (2, 2), (0, 0)],
        [(4, 3), (3, 4), (3, 3), (4, 4)],
    )
    paths = list(reversed(paths))
    paths = np.array(paths) / 2
    swarm = Crazyswarm(log_poses=False)
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    for cf in allcfs.crazyflies:
        cf.takeoff(targetHeight=1.0, duration=TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION + 1.0)

    for i, cf in enumerate(allcfs.crazyflies):
        pos = (*paths[i][0], 1.0)
        cf.goTo(pos, 0, 3.0)
    timeHelper.sleep(3.0)

    for t in range(len(paths[0])):
        for i, cf in enumerate(allcfs.crazyflies):
            pos = (*paths[i][t], 1.0)
            cf.goTo(pos, 0, 1.5)
        timeHelper.sleep(1.5)

    for cf in allcfs.crazyflies:
        cf.land(targetHeight=0.0, duration=2.5)
    timeHelper.sleep(2.5)


if __name__ == "__main__":
    main()
