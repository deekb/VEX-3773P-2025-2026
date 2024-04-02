from VEXLib.Robot.TelemteryRobot import TelemetryTickBasedRobot
from vex import Motor, GearSetting, Ports


# print = Telemetry.Telemetry.send_telemetry_message


class Robot(TelemetryTickBasedRobot):
    def __init__(self, brain):
        super().__init__(brain)
        self.motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
        self.i = int(0)

    def setup(self):
        print("Setup")
        self.register_telemetry()

    def on_enable(self):
        print("Enable")

    def periodic(self):
        # if not self.i % 10:
        print(("autonomous" if self.is_autonomous_control() else "driver control") + " " + ("enabled" if self.is_enabled() else "disabled"))
        print("runtime:" + str(self.get_enabled_runtime()))
        self.tick_telemetry()
        self.telemetry.send_telemetry_message("", "ROBOT_HEARTBEAT")
        # self.i += 1
        if self.get_enabled_runtime() > 3.0:
            self.trigger_restart()
