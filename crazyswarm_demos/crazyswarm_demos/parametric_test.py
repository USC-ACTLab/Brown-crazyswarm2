from crazyflie_py import Crazyswarm
import numpy as np

Hz = 20

def fx(t):
    # Parametric Equation defining y location at some time t
    return 0.0 # TODO
    # Parametric Equation defining x location at some time t
    # Note: if you need sin, cos, they are provided by numpy (np)
    # Just call np.sin(t) or np.cos(t)

def fy(t):
    t = t/3
    return (np.sin(t/2)*(np.exp(np.cos(t/2)) - 2*np.cos(4*t/2) - np.sin(t/2/12)**5))*0.6 # TODO


def fz(t):
    t = t/3
    # Parametric Equation defining z location at some time t
    return ((((np.cos(t/2)*(np.exp(np.cos(t/2)) - 2*np.cos(4*t/2) - np.sin(t/2/12)**5))+1.8)/4.9)*1.8)+0.25 # TODO

def main():
    # Initialize Swarm
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper

    # Grab the first crazyflie available
    cf = swarm.allcfs.crazyflies[0]
    cf.setParam('ring.effect', 7)
    cf.setLEDColor(0, 0, 0)

    start_time = 0 # TODO
    end_time = 12 * np.pi # TODO

    timesteps = np.arange(start_time, end_time + 1/Hz, 1/Hz)

    # Takeoff
    cf.takeoff(targetHeight=1.0, duration=2.5)
    timeHelper.sleep(3.5)

    # Navigate to start of trajectory
    t0 = timesteps[0]
    start_of_trajectory = (float(fx(t0)), float(fy(t0)), float(fz(t0)))
    cf.goTo(start_of_trajectory, 0.0, 5.0)
    timeHelper.sleep(6.0)

    # Set Color for trajectory
    cf.setLEDColor(160, 32, 240)
    timeHelper.sleep(0.5)

    # Begin trajectory
    for t in timesteps:
        cf.cmdPosition((float(fx(t)), float(fy(t)), float(fz(t))))
        timeHelper.sleepForRate(Hz)
    timeHelper.sleep(1.0)
    cf.setLEDColor(0, 0, 0)
    cf.notifySetpointsStop()
    cf.goTo(np.array(cf.initialPosition)+np.array([0., 0., 1.]), 0, 5.0)
    timeHelper.sleep(5.0)
    cf.land(targetHeight=0.04, duration=2.5)
    timeHelper.sleep(2.5)

if __name__ == '__main__':
    main()