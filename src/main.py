from Robot import Robot
from vex import Brain
from vex import Thread
from VEXLib.Network.Telemetry import Telemetry, TelemetryEntry
from VEXLib.Util import time

time.sleep(0.2)  # Don't print data over the REPL header
print()

robot = Robot(Brain())
print("Starting robot")

Thread(robot.start)


class CompetitionStateEntry(TelemetryEntry):
    def __init__(self, telemetry, robot):
        super().__init__(telemetry, "Competition State")
        self.robot = robot

    def get_value(self):
        return ("autonomous" if self.robot.is_autonomous_control() else "driver control") + " " + ("enabled" if self.robot.is_enabled() else "disabled")


telemetry = Telemetry()

competition_state_entry = CompetitionStateEntry(telemetry, robot)

while True:
    time.sleep(0.1)
    telemetry.update()
