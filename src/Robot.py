from VEXLib.Robot.TelemteryRobot import TelemetryRobot
from VEXLib.Robot.TimedRobot import TimedRobot
from vex import Motor, GearSetting, Ports


class Robot(TelemetryRobot, TimedRobot):
    def __init__(self, brain):
        self.brain = brain
        super().__init__(brain)
        self.motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)

    def setup(self):
        print("Setup")
        self.register_telemetry()

    def on_enable(self):
        print("Enable")

    def periodic(self):
        self.tick_telemetry()
        self.telemetry.send_message(("autonomous" if self.is_autonomous_control() else "driver control") + " " + ("enabled" if self.is_enabled() else "disabled"))
        self.telemetry.send_message("runtime:" + str(self.time_since_enable()))
        self.telemetry.send_message("ROBOT_HEARTBEAT")
        if self.time_since_enable() > 3.0:
            self.trigger_restart()
