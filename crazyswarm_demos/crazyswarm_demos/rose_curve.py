from crazyflie_py import Crazyswarm
import numpy as np
from crazyflie_py.uav_trajectory import Trajectory
from crazyflie_py.generate_trajectory import *
import os

TAKEOFF_DURATION = 2.
HOVER_DURATION = 2.5
TIMESCALE = 2.0
ALPHA = 0.5
N = 5
D = 4
K = N/D

def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    fx = lambda x: ALPHA * np.cos(K * x) * np.cos(x)
    fy = lambda x: 0 # 0.5 * np.sin(x)
    fz = lambda x: ALPHA * np.cos((K * x)) * np.sin(x)

    print("Generating Position Data")
    # TODO: Determine domain... (pi * n_leaves)
    offset = (np.pi / K)
    if N % 2 == 0 and D % 2 == 0:
        n_petals = N
    else:
        n_petals = 2*N

    pos_data = generate_position_data(fx, fy, fz, domain=(offset, np.pi*n_petals + offset))

    print("Computing trajectory")
    filename = f'data/rose_{ALPHA}_{K}.csv'
    if os.path.exists(filename):
        traj = Trajectory()
        traj.loadcsv(filename)    
    else:
        traj = generate_trajectory(pos_data, num_pieces=10)
        traj.savecsv(filename)
    traj.plot()
    print("Beginning CF execution")
    for cf in allcfs.crazyflies:
        cf.uploadTrajectory(0, 0, traj)
    timeHelper.sleep(1.0)
    allcfs.takeoff(targetHeight=1., duration=2.)
    timeHelper.sleep(4.0)
    
    allcfs.startTrajectory(0, timescale=TIMESCALE)
    timeHelper.sleep(traj.duration * TIMESCALE + 2.0)
    
    allcfs.land(targetHeight=0.04, duration=2.0)

if __name__ == "__main__":
    main()
