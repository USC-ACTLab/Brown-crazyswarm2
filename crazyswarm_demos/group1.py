from crazyflie_py import Crazyswarm
import numpy as np

Hz = 20
a= 10
b = 7
def fx(t):
    return 0.0

def fy(t):
    if t < 11*np.pi:
        return 0.07/2 * ((a-b) * np.cos(t) + b*np.cos((a/b - 1)*t)) # TODO
    else:
        t/=2
        return 0.07/2 * ((a+b) * np.cos(t) - b*np.cos((a/b + 1)*t))

def fz(t):
    if t < 11*np.pi: 
        return 0.07/2 * (((a-b) * np.sin(t) - b*np.sin((a/b - 1)*t))-20) + 1.75 # TODO
    else:
        t/=2
        return 0.07/2 * (((a+b) * np.sin(t) - b*np.sin((a/b + 1)*t))-20) + 1.75

def main():
    # Initialize Swarm
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper

    # Grab the first crazyflie available
    cf = swarm.allcfs.crazyflies[0]

    start_time = 0 # TODO
    end_time = 150 # TODO

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
    cf.setLEDColor(255, 255, 0)

    # Begin trajectory
    second = False
    for t in timesteps:
        if t >= 11*np.pi and not second:
            second = True
            cf.notifySetpointsStop()
            timeHelper.sleep(0.5)
            cf.setLEDColor(0, 0, 0)
            cf.goTo((fx(t), fy(t), fz(t)), 0.0, 3.0)
            timeHelper.sleep(3.5)
            cf.setLEDColor(0, 255, 255)
        cf.cmdPosition((fx(t), fy(t), fz(t)))
        timeHelper.sleepForRate(Hz)
    timeHelper.sleep(1.0)
    cf.notifySetpointsStop()
    cf.setLEDColor(0, 0, 0)
    cf.goTo(np.array(cf.initialPosition)+np.array([0.0, 0.0, 1.0]), 0, 5.0)
    timeHelper.sleep(5.0)
    cf.land(targetHeight=0.04, duration=2.5)
    timeHelper.sleep(2.5)

if __name__ == '__main__':
    main()