"""
This file is where the robot class is imported and instantiated from
"""

from VEXLib.Algorithms.PIDF import PIDFController
from VEXLib.Algorithms.PID import PIDController
from VEXLib.Math.MathUtil import MathUtil
from VEXLib.Robot.TelemteryRobot import TelemetryRobot
from VEXLib.Robot.TimedRobot import TimedRobot
from VEXLib.Units.Units import Units
from VEXLib.Util import time
from vex import *


class Robot(TelemetryRobot, TimedRobot):
    def __init__(self, brain):
        super().__init__(brain)
        self.left_drivetrain_1 = Motor(Ports.PORT1, GearSetting.RATIO_6_1, True)
        self.left_drivetrain_2 = Motor(Ports.PORT2, GearSetting.RATIO_6_1, True)
        self.left_drivetrain_3 = Motor(Ports.PORT3, GearSetting.RATIO_6_1, True)

        self.right_drivetrain_1 = Motor(Ports.PORT4, GearSetting.RATIO_6_1, False)
        self.right_drivetrain_2 = Motor(Ports.PORT5, GearSetting.RATIO_6_1, False)
        self.right_drivetrain_3 = Motor(Ports.PORT6, GearSetting.RATIO_6_1, False)

        self.controller = Controller(PRIMARY)

        self.left_drivetrain_PID = PIDFController(0.2, 0.15, 0.0, 0.175, 0.01, 6)
        self.right_drivetrain_PID = PIDFController(0.2, 0.15, 0.0, 0.175, 0.01, 6)

        # self.left_drivetrain_PID = PIDController(0.2, 0.1, 0.0, 0.01, 100, 0.1)
        # self.right_drivetrain_PID = PIDController(0.2, 0.1, 0.0, 0.01, 100, 0.1)


        self.i = 0

    def set_drivetrain_effort(self, left_effort, right_effort):
        self.left_drivetrain_1.spin(FORWARD, left_effort, VOLT)
        self.left_drivetrain_2.spin(FORWARD, left_effort, VOLT)
        self.left_drivetrain_3.spin(FORWARD, left_effort, VOLT)
        self.right_drivetrain_1.spin(FORWARD, right_effort, VOLT)
        self.right_drivetrain_2.spin(FORWARD, right_effort, VOLT)
        self.right_drivetrain_3.spin(FORWARD, right_effort, VOLT)

    @staticmethod
    def get_motor_speed_rad_per_sec(motor):
        return Units.rotations_per_minute_to_radians_per_second(motor.velocity(RPM))

    def get_left_drivetrain_speed(self):
        return MathUtil.average(self.get_motor_speed_rad_per_sec(self.left_drivetrain_1),
                                self.get_motor_speed_rad_per_sec(self.left_drivetrain_2),
                                self.get_motor_speed_rad_per_sec(self.left_drivetrain_3))

    def get_right_drivetrain_speed(self):
        return MathUtil.average(self.get_motor_speed_rad_per_sec(self.right_drivetrain_1),
                                self.get_motor_speed_rad_per_sec(self.right_drivetrain_2),
                                self.get_motor_speed_rad_per_sec(self.right_drivetrain_3))

    def update_efforts_from_target_speed(self, left_speed_rad_per_sec, right_speed_rad_per_sec):
        self.left_drivetrain_PID.setpoint = left_speed_rad_per_sec
        self.right_drivetrain_PID.setpoint = right_speed_rad_per_sec
        left_controller_output = self.left_drivetrain_PID.update(self.get_left_drivetrain_speed())
        right_controller_output = self.right_drivetrain_PID.update(self.get_right_drivetrain_speed())

        self.telemetry.send_message("LEFT_PID:IN=" + str(self.get_left_drivetrain_speed()) + ":TARG=" + str(
            self.left_drivetrain_PID.setpoint) + ":OUT=" + str(left_controller_output) + ":PROP=" + str(
            self.left_drivetrain_PID.kp)+ ":INTEGRAL=" + str(
            self.left_drivetrain_PID._error_integral))
        # self.telemetry.send_message("RIGHT_PID:IN=" + str(self.get_right_drivetrain_speed()) + ":TARG=" + str(
        #     self.right_drivetrain_PID.setpoint) + ":OUT=" + str(right_controller_output) + ":PROP=" + str(
        #     self.right_drivetrain_PID.kp))

        self.set_drivetrain_effort(left_controller_output, right_controller_output)
        time.sleep(0.01)

    def setup(self):
        self.register_telemetry()

    def periodic(self):
        self.tick_telemetry()
        if self.telemetry.serial.peek():
            if "LEFT_EFFORT" in self.telemetry.serial.peek():
                message = self.telemetry.serial.receive(True)

                self.set_drivetrain_effort(float(message.split(":")[1]), 0)
                self.telemetry.serial.send("ACK->LEFT_EFFORT")
            elif "ROBOT:RESTART" in self.telemetry.serial.peek():
                self.telemetry.serial.receive(True)
                self.telemetry.serial.send("ACK->ROBOT:RESTART")
                self.trigger_restart()
            elif "PID" in self.telemetry.serial.peek():
                message = self.telemetry.serial.receive(True)
                """PID:SET:left_drivetrain_PID:kf:0.10"""
                self.telemetry.serial.send("PID_ACK->" + str(message))
                _, action, name, *remaining = message.split(":")

                self.telemetry.serial.send("PID_ACK_ACTION->" + str(action))

                if action == "SET":
                    self.telemetry.serial.send("PID_ACK_SET")
                    attribute_name, attribute_value = remaining
                    self.set_PID_property(name, attribute_name, float(attribute_value))
                    self.telemetry.serial.send("PID_ACK_COMPLETE")
                elif action == "GET":
                    self.telemetry.serial.send("PID_ACK_GET")

                    attribute_name = remaining
                else:
                    self.telemetry.serial.send("PID_NACK_ACTION_INVALID")

            else:
                self.telemetry.serial.send("NACK->" + self.telemetry.serial.receive(True))
        # print(self.telemetry.serial.peek())

        # target_speed = random.randint(-60, 60)
        # start_time = time.time()
        # while time.time() - start_time < 2:
        self.update_efforts_from_target_speed(self.controller.axis3.position() * 70/100, self.controller.axis2.position() * 70/100)

        # if not self.i % 20:
        #     self.telemetry.send_message(("autonomous" if self.is_autonomous_control() else "driver control") + " " + ("enabled" if self.is_enabled() else "disabled"))
        #     self.telemetry.send_message("runtime:" + str(self.time_since_enable()))
        # self.i += 1
