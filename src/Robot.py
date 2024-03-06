from VEXLib.Robot import RobotBase


class Robot(RobotBase):
    def __init__(self, brain):
        super().__init__(brain)

    def setup(self):
        print("Setup")

    def on_enable(self):
        print("Enable")
