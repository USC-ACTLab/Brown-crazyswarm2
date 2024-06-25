import numpy as np
from crazyflie_py import *
import matplotlib.pyplot as plt
import pandas as pd
import pickle as pk
import scipy.io
import datetime


def main():
    Z = 1.0
    SEPARATION = 0.15

    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    positionsToGo = [(2.5, 0.0, Z + SEPARATION), (0.0, 0.0, Z)]

    for cf, pos in zip(allcfs.crazyflies, positionsToGo):
        # pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
        cf.takeoff(targetHeight=pos[2], duration=1.5 + Z)
    timeHelper.sleep(2.0 + Z)
    for cf, pos in zip(allcfs.crazyflies, positionsToGo):
        # pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
        cf.goTo(pos, 0.0, 21.0)

    timeHelper.sleep(21.0)

    allcfs.land(targetHeight=0.04, duration=1.0 + Z)
    timeHelper.sleep(1.5 + Z)

    # for cf in allcfs.crazyflies:
    #     poses = cf.poses

    # x1 = [p["cf67"][0][0] for p in poses]
    # x2 = [p["cf62"][0][0] for p in poses]
    # y1 = [p["cf67"][0][1] for p in poses]
    # y2 = [p["cf62"][0][1] for p in poses]
    # z1 = [p["cf67"][0][2] for p in poses]
    # z2 = [p["cf62"][0][2] for p in poses]

    # # orientation
    # # this all are error variables, they get nothoing
    # r1 = [p["cf67"][1][0] for p in poses]
    # r2 = [p["cf62"][1][0] for p in poses]
    # p1 = [p["cf67"][1][1] for p in poses]
    # p2 = [p["cf62"][1][1] for p in poses]
    # s1 = [p["cf67"][1][2] for p in poses]
    # s2 = [p["cf62"][1][2] for p in poses]
    # t = np.arange(0, len(x2) / 150, 1 / 150)

    # states = [t, x1, x2, y1, y2, z1, z2, r1, r2, p1, p2, s1, s2]

    # stacked_array = np.vstack(states)

    # scipy.io.savemat(
    #     "experiment_data/downwash_crossing_{}_sep_{}_m.mat".format(
    #         datetime.datetime.now(), SEPARATION
    #     ),
    #     {"states_array": stacked_array, "separation": np.array(SEPARATION)},
    #     do_compression=False,
    # # )

    # plt.plot(t, x1)
    # plt.plot(t, x2)
    # plt.show()

    allcfs.crazyflies[0].takeoff(1.0, 2.0)
    timeHelper.sleep(2.5)
    allcfs.crazyflies[0].goTo([-2.5, 0.0, 1.0], 0.0, 10.0)
    timeHelper.sleep(10.0)
    allcfs.land(targetHeight=0.04, duration=1.0 + Z)


if __name__ == "__main__":
    main()
