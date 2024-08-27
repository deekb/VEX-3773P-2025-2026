import json

from VEXLib.Robot.TelemteryRobot import TelemetryRobot
from VEXLib.Robot.TimedRobot import TimedRobot
from Drivetrain import Drivetrain
from MobileGoalClamp import MobileGoalClamp
from ScoringMechanism import ScoringMechanism
from vex import *


class Robot(TelemetryRobot, TimedRobot):
    def __init__(self, brain):
        super().__init__(brain)
        self.controller = Controller(PRIMARY)
        self.drivetrain = Drivetrain()
        self.left_distance_sensor = Distance(Ports.PORT5)
        self.right_distance_sensor = Distance(Ports.PORT4)
        self.i = 0
        self.mobile_goal_clamp = MobileGoalClamp()
        self.scoring_mechanism = ScoringMechanism(35, 100)

    def setup(self):
        self.register_telemetry()
        self.controller.buttonA.pressed(self.mobile_goal_clamp.toggle_clamp)
        self.controller.buttonUp.pressed(self.scoring_mechanism.retract_piston)
        self.controller.buttonDown.pressed(self.scoring_mechanism.extend_piston)

        # while not self.brain.screen.pressing():
        #     pass
        # self.drivetrain.turn_to_gyro(0)
        # self.drivetrain.turn_to_gyro(90)
        # self.drivetrain.turn_to_gyro(-90)

    def periodic(self):
        # self.tick_telemetry()
        # if self.telemetry.serial.peek():
        #     if "ROBOT:RESTART" in self.telemetry.serial.peek():
        #         self.telemetry.serial.receive(True)
        #         self.telemetry.serial.send("ACK->ROBOT:RESTART")
        #         self.trigger_restart()
        #     else:
        #         self.telemetry.serial.send("NACK->" + self.telemetry.serial.receive(True))

        # Arcade drive calculations
        left_speed = self.controller.axis3.position()
        right_speed = self.controller.axis2.position()
        pto_speed = self.controller.axis1.position()
        wiggle = self.controller.buttonX.pressing()

        # left_speed = forward + rotation
        # right_speed = forward - rotation

        self.drivetrain.set_speed_percent(left_speed, right_speed)
        self.drivetrain.update_motor_voltages()
        self.drivetrain.update_odometry()

        if wiggle:
            self.scoring_mechanism.wiggle()
        else:
            self.scoring_mechanism.spin_motor_at_speed(pto_speed)

        telemetry_frame = {"odometry_position": self.drivetrain.current_position,
                           "odometry_rotation": self.drivetrain.current_rotation}

        print(json.dumps(telemetry_frame))
        print("Frame tx finish")

        # if not self.i % 3:
        #     self.telemetry.send_message(self.left_distance_sensor.object_distance(MM))
        #     self.telemetry.send_message(self.right_distance_sensor.object_distance(MM))
        # self.i += 1
