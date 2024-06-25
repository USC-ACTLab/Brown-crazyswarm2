from crazyflie_py import Crazyswarm
import numpy as np

Z = 1.0
waveHeight = 0.5


def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

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

    allcfs.takeoff(targetHeight=Z, duration=1.0 + Z)
    timeHelper.sleep(1.5 + Z)

    x = 0
    for cf in allcfs.crazyflies:
        pos = np.array([x, 0.0, Z])
        cf.goTo(pos, 0, 2.0)
        x = x - 0.5
    timeHelper.sleep(2.0)

    # wave from right to left
    time = 0
    for cf in allcfs.crazyflies:
        position = cf.position()
        pos = np.array(position) + np.array([0.0, 0.0, waveHeight])
        cf.goTo(pos, 0, 2.0)
        timeHelper.sleep(0.25)
        time = time + 0.25
    if time < 2.0:
        timeHelper.sleep(2.0 - time)

    for cf in allcfs.crazyflies:
        position = cf.position()
        pos = np.array(position) - np.array([0.0, 0.0, waveHeight])
        cf.goTo(pos, 0, 2.0)
        timeHelper.sleep(0.25)
    timeHelper.sleep(1.75)

    # opposite wave, from left to right
    sorted_cfs = sorted(
        [(cf.initialPosition[0], np.random.uniform(), cf) for cf in allcfs.crazyflies]
    )
    cfs = []
    for p, r, cf in sorted_cfs:
        cfs.append(cf)
    allcfs.crazyflies_reveresed = cfs

    for cf in allcfs.crazyflies_reveresed:
        # how to get the updated current positions at this stage?
        position = cf.position()
        pos = np.array(position) - np.array([0.0, 0.0, waveHeight])
        cf.goTo(pos, 0, 2.0)
        timeHelper.sleep(0.25)
    if time < 2.0:
        timeHelper.sleep(2.0 - time)

    for cf in allcfs.crazyflies_reveresed:
        position = cf.position()
        pos = np.array(position) + np.array([0.0, 0.0, waveHeight])
        cf.goTo(pos, 0, 2.0)
        timeHelper.sleep(0.25)
    timeHelper.sleep(1.75)

    allcfs.land(targetHeight=0.04, duration=2.5)
    timeHelper.sleep(2.5)


if __name__ == "__main__":
    main()
