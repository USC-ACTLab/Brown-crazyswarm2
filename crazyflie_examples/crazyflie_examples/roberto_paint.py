"""Takeoff-hover-land for one CF. Useful to validate hardware config."""

# from pycrazyswarm import Crazyswarm
from crazyflie_py import Crazyswarm
import pickle

TAKEOFF_DURATION = 5.5
HOVER_DURATION = 5.0


def main():
    swarm = Crazyswarm(log_poses=False)
    timeHelper = swarm.timeHelper
    cf = swarm.allcfs.crazyflies[0]

    cf.takeoff(targetHeight=1.0, duration=TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION + HOVER_DURATION)
    # cf.goTo((0.5, 0.0, 1.0), 0, 3)
    # timeHelper.sleep(3)
    for i in range(100, 45, -1):
        print(i)
        cf.setParam("servo.servoAngle", i)
        timeHelper.sleep(0.5)
    # cf.goTo((0.0, 0.0, 1.0), 0.0, 3)
    # timeHelper.sleep(3.5)
    cf.land(targetHeight=0.35, duration=2.5)
    timeHelper.sleep(TAKEOFF_DURATION)
    # save the name based on test specs
    # pickle.dump(cf.poses, open("single_cf.p","wb"))
    # print(cf.poses)
    # with open('single.p', 'rb') as f:
    #     x = pickle.load(f)


if __name__ == "__main__":
    main()
