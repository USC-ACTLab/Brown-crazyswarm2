from crazyflie_py import Crazyswarm
import numpy as np

Hz = 20

def fx(t):
    return 0 # TODO

def fy(t):
    return 0 # TODO

def fz(t):
    return 0 # TODO

def main():
    # Initialize Swarm
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper

    # Grab the first crazyflie available
    cf = swarm.allcfs.crazyflies[0]

    start_time = 0 # TODO
    end_time = 2*np.pi # TODO

    timesteps = np.arange(start_time, end_time + 1/Hz, 1/Hz)

    # Takeoff
    cf.takeoff(targetHeight=1.0, duration=2.5)
    timeHelper.sleep(3.5)

    # Navigate to start of trajectory
    t0 = timesteps[0]
    start_of_trajectory = (fx(t0), fy(t0), fz(t0))
    cf.goTo(start_of_trajectory, 0.0, 5.0)
    timeHelper.sleep(6.0)

    # Begin trajectory
    for t in timesteps:
        cf.cmdPosition((fx(t), fy(t), fz(t)))
        timeHelper.sleepForRate(Hz)
    timeHelper.sleep(1.0)
    cf.notifySetpointsStop()
    cf.goTo(np.array(cf.initialPosition)+np.array([0, 0, 1]), 0, 5.0)
    timeHelper.sleep(5.0)
    cf.land(targetHeight=0.04, duration=2.5)
    timeHelper.sleep(2.5)

if __name__ == '__main__':
    main()