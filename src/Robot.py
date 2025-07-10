from VEXLib.Robot.RobotBase import RobotBase
from VEXLib.Util import time


class Robot(RobotBase):
    def __init__(self, brain):
        super().__init__(brain)

    def on_driver_control(self):
        while True:
            self.driver_control_periodic()
            time.sleep_ms(20)

    def driver_control_periodic(self):
        ...