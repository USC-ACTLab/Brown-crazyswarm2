from crazyflie_py import Crazyswarm
import numpy as np
Hz = 10
lorenz_Hz = 100

sigma = 10
rho = 28
beta = 8/3

def get_next_setpoints(x, y, z, world_translate=[0, 0, 0.25], initial_position_lorenz=[6, 12, 24], scaler=25):
    dx = fx1(x, y, z) / lorenz_Hz
    dy = fy1(x, y, z) / lorenz_Hz
    dz = fz1(x, y, z) / lorenz_Hz

    x = x * scaler


def fx1(x, y, z):
    return  sigma * (y - x)# TODO

def fy1(x, y, z):
    return x * (rho - z) - y # TODO

def fz1(x, y, z):
    return x * y - beta * z # TODO

def main():
    # Initialize Swarm
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    sim = False
    # Grab the first crazyflie available
    cfs = swarm.allcfs.crazyflies
    cfs = reversed(sorted([(cf.initialPosition[0], np.random.uniform(), cf) for cf in swarm.allcfs.crazyflies]))
    cfs = [cf[2] for cf in cfs]

    start_time = 0 # TODO
    end_time = 120 # TODO

    timesteps = np.arange(start_time, end_time + 1/Hz, 1/Hz)
    trajectories = [(fx1, fy1, fz1)]

    colors = [(0, 255, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (0, 255, 255)]
    # Takeoff
    if not sim:
        for cf in cfs:
            cf.setLEDColor(0, 0, 0)
    timeHelper.sleep(0.5)

    

    for cf in cfs:
        cf.takeoff(targetHeight=1.0, duration=2.5)
    
    timeHelper.sleep(3.5)

    # Navigate to start of trajectory
    x = 6
    y = 12
    z = 11.5
    for cf, (fx, fy, fz) in zip(cfs, trajectories):
        cf.goTo((x/25, y/25, z/25+0.5), 0, 5.0)
    timeHelper.sleep(6.0)

    # Set correct Color
    if not sim:
        for cf, color in zip(cfs, colors):
            cf.setLEDColor(*color)
    xs, ys ,zs = [], [], []

    # Begin trajectory
    for t in timesteps:
        for cf, (fx, fy, fz) in zip(cfs, trajectories):
            dx = fx(x, y, z)*1/lorenz_Hz
            dy = fy(x, y, z)*1/lorenz_Hz
            dz = fz(x, y, z)*1/lorenz_Hz
            x += dx
            y += dy
            z += dz
            pos = cf.position()
            alt_x = pos[0]*25 + dx
            alt_y = pos[1]*25 + dy
            alt_z = (pos[2]-0.5)*25 + dz
            print(x, alt_x, y, alt_y, z, alt_z)
            cf.cmdPosition((x/25, y/25, z/25+0.25))
        timeHelper.sleepForRate(Hz)
    timeHelper.sleep(1.0)

    for cf in cfs:
        if not sim:
            cf.setLEDColor(0, 0, 0)
        cf.notifySetpointsStop()
        cf.goTo(np.array(cf.initialPosition)+np.array([0., 0., 1.]), 0, 5.0)
    timeHelper.sleep(5.0)
    
    for cf in cfs:
        cf.land(targetHeight=0.04, duration=2.5)
    timeHelper.sleep(2.5)

if __name__ == '__main__':
    main()
