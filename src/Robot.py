import json

from VEXLib.Robot.TelemteryRobot import TelemetryRobot
from VEXLib.Robot.TimedRobot import TimedRobot
from VEXLib.Util import time
from Drivetrain import Drivetrain
from MobileGoalClamp import MobileGoalClamp
from ScoringMechanism import ScoringMechanism
from SerialData import Frame
from CRC import crc_bytes
from vex import *


class Robot(TimedRobot):
    def __init__(self, brain):
        super().__init__(brain)
        self.controller = Controller(PRIMARY)
        self.drivetrain = Drivetrain()
        self.left_distance_sensor = Distance(Ports.PORT5)
        self.right_distance_sensor = Distance(Ports.PORT4)
        self.i = 0
        self.mobile_goal_clamp = MobileGoalClamp()
        self.scoring_mechanism = ScoringMechanism(35, 100)
        # self.file_handle = open("/dev/port20", "rwb")

        # self.output_buffer = []
        # self.input_buffer = []
        #
        # self.has_token = False

    def setup(self):
        # self.register_telemetry()
        self.controller.buttonA.pressed(self.mobile_goal_clamp.toggle_clamp)
        self.controller.buttonUp.pressed(self.scoring_mechanism.retract_piston)
        self.controller.buttonDown.pressed(self.scoring_mechanism.extend_piston)

        # while not self.brain.screen.pressing():
        #     pass
        # self.drivetrain.turn_to_gyro(0)
        # self.drivetrain.turn_to_gyro(90)
        # self.drivetrain.turn_to_gyro(-90)

    # def process_message(self, message):
    #

    def periodic(self):
        # if self.has_token:
        #     # If we have the token either send a message and pass off the token or just pass off the token
        #     if self.output_buffer:
        #         self.file_handle.write(self.output_buffer.pop(0).encode() + b"TKN\n")
        #         self.has_token = False
        #     else:
        #         self.file_handle.write(b"{}TKN\n")
        #         self.has_token = False
        # else:
        #     # If we don't have the token, just listen
        #     data = self.file_handle.readline().decode()
        #     if data != "":
        #         self.input_buffer.append(data.rstrip("TKN\n"))
        #         if "TKN" in data:
        #             self.has_token = True
        #             print(self.input_buffer)
        #             self.output_buffer.append(str({"Status": "Got message"}))
        #             self.input_buffer.clear()

        # frame = Frame(frame_header=[0xEB, 0x90], frame_type=0x3, data_length=len("hello world"), frame_id=1,
        #               data="This is a test message", crc_function=crc_bytes)
        # frame_bytearray = frame.get_bytearray()
        # self.file_handle.write(frame_bytearray)
        # print(frame_bytearray.hex().upper())
        # print(frame_bytearray)

        left_speed = self.controller.axis3.position()
        right_speed = self.controller.axis2.position()
        pto_speed = self.controller.axis1.position()
        wiggle = self.controller.buttonX.pressing()

        self.drivetrain.set_speed_percent(left_speed, right_speed)
        self.drivetrain.update_motor_voltages()
        self.drivetrain.update_odometry()
        print(self.drivetrain.odometry.pose)

        if wiggle:
            self.scoring_mechanism.wiggle()
        else:
            self.scoring_mechanism.spin_motor_at_speed(pto_speed)
