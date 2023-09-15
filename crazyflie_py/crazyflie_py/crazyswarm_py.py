import rclpy

from . import genericJoystick
from .crazyflie import TimeHelper, CrazyflieServer


class Crazyswarm:
    def __init__(self, log_poses=False):
        rclpy.init()
        
        self.allcfs = CrazyflieServer(log_poses=log_poses)
        self.timeHelper = TimeHelper(self.allcfs)

        self.input = genericJoystick.Joystick(self.timeHelper)
