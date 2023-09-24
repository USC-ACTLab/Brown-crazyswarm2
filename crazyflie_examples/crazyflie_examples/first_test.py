import numpy as np

# V1
#from pycrazyswarm import *
# V2
from crazyflie_py import Crazyswarm

# Environment constants
Z = 1.0
TAKEOFF_DURATION = 2.5
TARGET_HEIGHT = 0.02
GOTO_DURATION = 3.0
LAND_DURATION = 3.0
TIME = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
WAYPOINTS_R1 = np.array([
    [0.5, 0.5, 0.5, 0.5, 1.0, 1.5, 1.5, 1.5, 1.5, 1.0],
    [0.0, 0.5, 1.0, 1.5, 1.5, 1.5, 1.0, 0.5, 0.0, 0.0],
    [Z, Z, Z, Z, Z, Z, Z, Z, Z, Z]
    ])
WAYPOINTS_R2 = np.array([
    [-1.0, -1.5, -2.0, -2.5, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [Z, Z, Z, Z, Z, Z, Z, Z, Z, Z]
    ])
num_drones = 2

def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    # Start the mission
    allcfs.takeoff(Z, TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION + 1)

    # Get the number of timesteps
    num_timesteps = len(TIME)

    # Assign positions to each drone at each timestep
    for t in range(num_timesteps):
        for i in range(num_drones):
            if i == 0: 
                # Get the positions for the current timestep 
                position = WAYPOINTS_R1[:, t] # Gets a vector of all the row values in a specifc column t
            else:
                # print("hi")
                position = WAYPOINTS_R2[:, t] 
            # Assign positions to each drone, TODO: generalize for an arbitrary number of drones
            cf = allcfs.crazyflies[i]
            cf.goTo([position[0], position[1], position[2]], 0.0, TIME[i] - TIME[i-1], False) 

        timeHelper.sleep(1.01)

    # Land the drones
    allcfs.land(TARGET_HEIGHT, LAND_DURATION)
    timeHelper.sleep(LAND_DURATION + 1)

def switch(i, t):
    if i == 0: 
        return WAYPOINTS_R1[:,t]
    # elif i == 1:
        

    
if __name__ == "__main__":
    main()
