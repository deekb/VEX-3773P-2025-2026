from VEXLib.Robot.TelemteryRobot import TelemetryRobot
from VEXLib.Robot.RobotBase import RobotBase
from VEXLib.Robot.TimedRobot import TimedRobot
from vex import Motor, GearSetting, Ports


# print = Telemetry.Telemetry.send_telemetry_message


class Robot(TelemetryRobot, TimedRobot):
    def __init__(self, brain):
        self.brain = brain
        super().__init__(brain)
        self.motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
        self.i = 0

    def setup(self):
        print("Setup")
        self.register_telemetry()

    def on_enable(self):
        print("Enable")

    def periodic(self):
        # if not self.i % 10:
        print(("autonomous" if self.is_autonomous_control() else "driver control") + " " + ("enabled" if self.is_enabled() else "disabled"))
        print("runtime:" + str(self.time_since_enable()))
        self.tick_telemetry()
        self.telemetry.send_telemetry_message("ROBOT_HEARTBEAT")
        self.i += 1
        if self.time_since_enable() > 3.0:
            self.trigger_restart()
