"""Takeoff-hover-land for one CF. Useful to validate hardware config."""

# from pycrazyswarm import Crazyswarm
from crazyflie_py import Crazyswarm
import pickle 

TAKEOFF_DURATION = 4.5
HOVER_DURATION = 1.0


def main():
    swarm = Crazyswarm(log_poses=False)
    timeHelper = swarm.timeHelper
    cf = swarm.allcfs.crazyflies[0]
    cf.takeoff(targetHeight=1.0, duration=TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION + HOVER_DURATION)

    # for i in range(3):
    #     cf.setParam('servo.servoAngle', -30)
    #     timeHelper.sleep(2.0)
    #     cf.setParam('servo.servoAngle', 0)
    #     timeHelper.sleep(2.0)

    for i in range(6):
        cf.setParam('servo.servoAngle', i*5)
        timeHelper.sleep(2.)

    for i in range(6):
        cf.setParam('servo.servoAngle', (6 - i)*5)
        timeHelper.sleep(2.)



    # cf.setParam('motorPowerSet.enable', 1)
    # cf.setParam('motorPowerSet.m1', 60000)
    # cf.setParam('motorPowerSet.m2', 60000)
    # cf.setParam('motorPowerSet.m3', 60000)
    # cf.setParam('motorPowerSet.m4', 60000)




    # for i in range(10):
    #     cf.setParam('')
    cf.land(targetHeight=0.04, duration=2.5)
    timeHelper.sleep(TAKEOFF_DURATION)
    #save the name based on test specs
    # pickle.dump(cf.poses, open("single_cf.p","wb"))
    # print(cf.poses)
    # with open('single.p', 'rb') as f:
    #     x = pickle.load(f)


if __name__ == "__main__":
    main()
