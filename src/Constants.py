import math

from VEXLib.Geometry.RotationalVelocity import RotationalVelocity
from VEXLib.Geometry.Translation1d import Distance
from vex import Ports, GearSetting, Brain


class SmartPorts:
    """Drivetrain"""
    FRONT_LEFT_DRIVETRAIN_MOTOR = Ports.PORT17
    MIDDLE_LEFT_DRIVETRAIN_MOTOR = Ports.PORT11
    REAR_LEFT_DRIVETRAIN_MOTOR = Ports.PORT1

    FRONT_RIGHT_DRIVETRAIN_MOTOR = Ports.PORT16
    MIDDLE_RIGHT_DRIVETRAIN_MOTOR = Ports.PORT13
    REAR_RIGHT_DRIVETRAIN_MOTOR = Ports.PORT15

    SCORING_MOTOR = Ports.PORT6

    INERTIAL_SENSOR = Ports.PORT12


class ThreeWirePorts:
    """Scoring Mechanism"""
    brain = Brain()
    PTO_PISTON = brain.three_wire_port.a
    MOBILE_GOAL_CLAMP_PISTON = brain.three_wire_port.b
    LIMIT_SWITCH = brain.three_wire_port.c
    del brain


class GearRatios:
    DRIVETRAIN = GearSetting.RATIO_6_1


class DrivetrainProperties:
    MAX_ACHIEVABLE_SPEED = RotationalVelocity.from_rotations_per_minute(600)
    MOTOR_TO_WHEEL_GEAR_RATIO = (36 / 60)
    TRACK_WIDTH = Distance.from_inches(13.5)
    WHEEL_DIAMETER = Distance.from_inches(3.235)
    WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER * math.pi
