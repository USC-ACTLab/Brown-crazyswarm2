from crazyflie_py import Crazyswarm
import numpy as np

def main():

    Z = 1.0

    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    for i in range(4):
        allcfs.crazyflies[i].takeoff(targetHeight=Z, duration=1.0+Z)
        timeHelper.sleep(1.0)

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0,0,Z])
        cf.goTo(pos,0,1.0)

    timeHelper.sleep(4.0)
    allcfs.land(targetHeight = 0.02, duration = Z + 1.0)

if __name__ == "__main__":
    main()