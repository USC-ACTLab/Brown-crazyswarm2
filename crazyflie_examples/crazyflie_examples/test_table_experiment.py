#!/usr/bin/env python

import numpy as np
import rospy
from std_msgs.msg import Float32
from crazyflie_py import *
from scipy.io import savemat


def main():
    # rospy initialization
    rospy.init_node("cf_data_logger")
    # pwm_pub = rospy.Publisher('/crazyflie/pwm_thrust', Float32, queue_size = 10)

    Z = 0.54

    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    data = {"Crazyflie": []}
    # pwm_vals = [[] for _ in range(len(allcfs.crazyflies))]

    allcfs.takeoff(targetHeight=Z, duration=1.0 + Z)
    timeHelper.sleep(1.5 + Z)
    # Move to start positions...
    for i, cf in enumerate(allcfs.crazyflies):
        if i == 0:
            rotation = np.pi / 4
        else:
            rotation = 0
        pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
        cf.goTo(pos, rotation, 5)
    timeHelper.sleep(5.5)

    # Cross the table...
    for i, cf in enumerate(allcfs.crazyflies):
        if i == 0:
            rotation = np.pi / 4
        else:
            rotation = 0
        pos = np.array(cf.initialPosition) + np.array([0, 2, Z])
        cf.goTo(pos, rotation, 10)
    timeHelper.sleep(10.5)

    # Cross the table...
    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
        cf.goTo(pos, 0.0, 10)
    timeHelper.sleep(10.5)

    allcfs.land(targetHeight=0.04, duration=1.0 + Z)
    timeHelper.sleep(1.5 + Z)

    for i, cf in enumerate(allcfs.crazyflies):
        cf_data = {"PWM": [], "Position": [], "Orientation": [], "Time": []}
        # pwm_thrust = cf.getPWM()
        # pwm_pub.publish(pwm_thrust)
        # pwm_vals[i].append(pwm_thrust)

        init_pos = np.array(cf.initialPosition)
        init_orient = cf.initialAttitude.q

        # Take off time
        takeoff_time = rospy.Time.now()

        # Store takeoff data
        cf_data["Position"].append(init_pos)
        cf_data["Orientation"].append(init_orient)
        cf_data["Time"].append(takeoff_time.to_sec())

        for pos_cmd in [(0, 0, Z), (0, 2, Z), (0, 0, Z)]:
            cf.goTo(init_pos + np.array(pos_cmd), 0, 10)
            timeHelper.sleep(10.5)

            # sTORING Pose and PWM
            pose = cf.position()
            orientation = cf.attitude().q
            pwm_thrust = cf.getPWM()
            current_time = rospy.Time.now()

            cf_data["PWM"].append(pwm_thrust)
            cf_data["Position"].append(pose)
            cf_data["Orientation"].append(orientation)
            cf_data["Time"].append(current_time.to_sec())

        data["Crazyflie"].append(cf_data)

    file_path = "/home/csci1951z/ros2_ws/src/Brown-crazyswarm2/crazyflie_examples/crazyflie_examples/crazyflie_data_test1.mat"
    savemat(file_path, data)

    print(f"Saved to {file_path}")


if __name__ == "__main__":
    main()
