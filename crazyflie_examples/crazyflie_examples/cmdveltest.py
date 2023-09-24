"""Takeoff-hover-land for one CF. Useful to validate hardware config."""

# from pycrazyswarm import Crazyswarm
from crazyflie_py import Crazyswarm
import numpy as np

TAKEOFF_DURATION = 2.5
HOVER_DURATION = 5.0


def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cf = swarm.allcfs.crazyflies[0]

    cf.takeoff(targetHeight=1.0, duration=TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION)
    
    for t in np.arange(0, 4*np.pi, 0.05):
        cf.cmdVelocityWorld((np.cos(t/2)/2, np.sin(t/2)/2, 0.), 0.)
        print((np.cos(t/2)/2, np.sin(t/2)/2, 0.), 0.)
        timeHelper.sleepForRate(20)
    cf.notifySetpointsStop()

    cf.goTo(cf.initialPosition + np.array([0., 0., 1.]), 0, 1.0)
    timeHelper.sleep(1.0)
    cf.land(0.0, 2.0)

if __name__ == "__main__":
    main()
