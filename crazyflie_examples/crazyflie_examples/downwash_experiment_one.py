import numpy as np
from crazyflie_py import *
import matplotlib.pyplot as plt
import pandas as pd
import pickle as pk
import scipy.io
import datetime
def main():
    Z = 1.0
    SEPARATION = 0.1
    
    swarm = Crazyswarm(log_poses=True)
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs
    
    positionsToGo = [(1.5, 0.,Z + SEPARATION), (0.,0.,Z)]
 
    for cf, pos in zip(allcfs.crazyflies, positionsToGo):
        # pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
        cf.takeoff(targetHeight=pos[2], duration=1.5+Z)
    timeHelper.sleep(2.0+Z)
    for cf, pos in zip(allcfs.crazyflies, positionsToGo):
        # pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
        cf.goTo(pos, 0., 5.0)
 
    
    timeHelper.sleep(6.0)

    allcfs.land(targetHeight=0.04, duration=1.0+Z)
    timeHelper.sleep(1.5+Z)
    
    for cf in allcfs.crazyflies:
        poses = cf.poses


    x1 = [p['cf29'][0][0] for p in poses]
    x2 = [p['cf62'][0][0] for p in poses]
    y1 = [p['cf29'][0][1] for p in poses]
    y2 = [p['cf62'][0][1] for p in poses]
    z1 = [p['cf29'][0][2] for p in poses]
    z2 = [p['cf62'][0][2] for p in poses]

    #orientation
    r1 = [p['cf29'][1][0] for p in poses]
    r2 = [p['cf62'][1][0] for p in poses]
    p1 = [p['cf29'][1][1] for p in poses]
    p2 = [p['cf62'][1][1] for p in poses]
    s1 = [p['cf29'][1][2] for p in poses]
    s2 = [p['cf62'][1][2] for p in poses]
    t = np.arange(0, len(x2)/150, 1/150)

    states = [t, x1, x2, y1, y2, z1, z2, r1, r2, p1, p2, s1, s2]


    stacked_array = np.vstack(states)

    # scipy.io.savemat('experiment_data/downwash_crossing_{}_sep_{}_m.mat'.format(datetime.datetime.now(), np.array(SEPARATION)), {'states_array': stacked_array,'separation': np.array(SEPARATION)}, do_compression=False)


    # data = {
    #     'x1': x1,
    #     'y1': y1,
    #     'z1': z1,
    #     'x2': x2,
    #     'y2': y2,
    #     'z2': z2
    # }
    
    # df = pd.DataFrame(data)
    # with open('experiment_data/data_table_{}.pkl'.format(datetime.datetime.now()), 'wb') as f:
    #     pk.dump({'data_table':df.to_dict(), 'separation': np.array(SEPARATION)}, f)
    # scipy.io.savemat('experiment_data/data_table_{}.mat'.format(datetime.datetime.now()), {'data_table':df.to_dict(), 'separation': np.array(SEPARATION)})
    # scipy.io.savemat('experiment_data/data_table_{}.mat'.format(datetime.datetime.now()), {'data_table': np.array(data), 'separation': np.array(SEPARATION)})
    # print(df.to_dict())
    plt.plot(t, x1)
    plt.plot(t, x2)
    plt.show()

    allcfs.crazyflies[0].takeoff(1.0, 2.0)
    timeHelper.sleep(2.5)
    allcfs.crazyflies[0].goTo([-1.5, 0., 1.], 0.0, 5.0)
    timeHelper.sleep(6.0)
    allcfs.land(targetHeight=0.04, duration=1.0+Z)



if __name__ == "__main__":
    main()