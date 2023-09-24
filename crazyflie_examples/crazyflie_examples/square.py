from crazyflie_py import Crazyswarm
import numpy as np

def main():
    Z = 1.0
    positions = [
    (0., 0., 1.0),
    (0., 1.0, 1.0),
    (1., 1.0, 1.0),
    (1., 0., 1.0),
    (0., 0., 1.0)
]
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cf = swarm.allcfs.crazyflies[0]

    cf.takeoff(targetHeight=Z, duration=1.0 + Z)
    
    timeHelper.sleep(1.0 + Z)

    for pos in positions:
        cf.goTo(pos,0,3.0)
        timeHelper.sleep(3.0)

    cf.land(targetHeight=0.02, duration=1.0 + Z)

if __name__ == "__main__":
    main()