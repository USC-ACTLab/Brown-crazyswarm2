from crazyflie_py import Crazyswarm
import numpy as np

Hz = 20


a = 8
b = 2
c = 3

def fx(t):
    return 0.0 # TODO


def fy(t):
    t /= 2
    return 0.1 * ((a-b) * np.cos(t) + c*np.cos((a/b - 1) * t)) # TODO


def fz(t):
    t /=2
    return 0.1 * ((a-b) * np.sin(t) - c*np.sin((a/b - 1)*t)) + 1.25 # TODO

def main():
    # Initialize Swarm
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper

    # Grab the first crazyflie available
    cf = swarm.allcfs.crazyflies[0]

    start_time = 0 # TODO
    end_time = 15 # TODO

    timesteps = np.arange(start_time, end_time + 1/Hz, 1/Hz)
    cf.setLEDColor(0, 0, 0)

    # Takeoff
    cf.takeoff(targetHeight=1.0, duration=2.5)
    timeHelper.sleep(3.5)

    # Navigate to start of trajectory
    t0 = timesteps[0]
    start_of_trajectory = (fx(t0), fy(t0), fz(t0))
    cf.goTo(start_of_trajectory, 0.0, 5.0)
    timeHelper.sleep(6.0)
    cf.setLEDColor(255, 0, 0)

    # Begin trajectory
    for t in timesteps:
        cf.cmdPosition((fx(t), fy(t), fz(t)))
        timeHelper.sleepForRate(Hz)
    timeHelper.sleep(1.0)
    cf.notifySetpointsStop()
    cf.setLEDColor(0, 0, 0)
    cf.goTo(np.array(cf.initialPosition)+np.array([0., 0., 1.]), 0, 5.0)
    timeHelper.sleep(5.0)
    cf.land(targetHeight=0.04, duration=2.5)
    timeHelper.sleep(2.5)

if __name__ == '__main__':
    main()