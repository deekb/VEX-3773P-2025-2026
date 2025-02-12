from VEXLib.Geometry.GeometryUtil import circle_circumference
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation1d import Distance
from VEXLib.Geometry.Velocity1d import Velocity1d
from vex import Ports, GearSetting, Brain

MAIN_LOG_FILENAME = "main"


class ControlStyles:
    TANK = 1
    ARCADE = 2
    SPLIT_ARCADE = 3


class DefaultPreferences:
    CONTROL_STYLE = ControlStyles.TANK
    CUBIC_FILTER_LINEARITY = 1
    MAX_MOTOR_VOLTAGE = 12
    TURN_SPEED = 1


class DirkPreferences(DefaultPreferences):
    CONTROL_STYLE = ControlStyles.SPLIT_ARCADE
    CUBIC_FILTER_LINEARITY = 1
    TURN_SPEED = 0.7


class DerekPreferences(DefaultPreferences):
    CONTROL_STYLE = ControlStyles.SPLIT_ARCADE
    CUBIC_FILTER_LINEARITY = 1


class AllisonPreferences(DefaultPreferences):
    CONTROL_STYLE = ControlStyles.SPLIT_ARCADE
    CUBIC_FILTER_LINEARITY = 1


class CarterPreferences(DefaultPreferences):
    CONTROL_STYLE = ControlStyles.TANK
    CUBIC_FILTER_LINEARITY = 1


class SmartPorts:
    """Drivetrain"""
    FRONT_LEFT_DRIVETRAIN_MOTOR = Ports.PORT17
    MIDDLE_LEFT_DRIVETRAIN_MOTOR = Ports.PORT11
    REAR_LEFT_DRIVETRAIN_MOTOR = Ports.PORT1

    FRONT_RIGHT_DRIVETRAIN_MOTOR = Ports.PORT16
    MIDDLE_RIGHT_DRIVETRAIN_MOTOR = Ports.PORT13
    REAR_RIGHT_DRIVETRAIN_MOTOR = Ports.PORT15

    SCORING_ELEVEN_WATT_MOTOR = Ports.PORT6
    SCORING_FIVE_POINT_FIVE_WATT_MOTOR = Ports.PORT3
    WALL_STAKE_MOTOR = Ports.PORT8

    INERTIAL_SENSOR = Ports.PORT11


class ThreeWirePorts:
    """Scoring Mechanism"""
    brain = Brain()
    MOBILE_GOAL_CLAMP_PISTON = brain.three_wire_port.b
    DOINKER_PISTON = brain.three_wire_port.c
    WALL_STAKE_CALIBRATION_LIMIT_SWITCH = brain.three_wire_port.d



class GearRatios:
    DRIVETRAIN = GearSetting.RATIO_6_1


class DrivetrainProperties:
    MAX_ACHIEVABLE_SPEED = Velocity1d.from_meters_per_second(2)
    MOTOR_TO_WHEEL_GEAR_RATIO = (36 / 60)
    WHEEL_DIAMETER = Distance.from_inches(3.235)
    WHEEL_CIRCUMFERENCE = circle_circumference(WHEEL_DIAMETER / 2)


class WallStakeMechanismProperties:
    PID_TUNINGS = {
        "kp": 50,
        "ki": 0,
        "kd": 1
    }
    FEEDFORWARD_TUNINGS = {
        "kg": 0.9
    }
    DOCKED_POSITION = Rotation2d.from_degrees(-100)
    DOCKED_TOLERANCE = Rotation2d.from_degrees(2)
    LOADING_POSITION = Rotation2d.from_degrees(-75)
    UPRIGHT_POSITION = Rotation2d.from_degrees(0)
    HIGH_SCORING_POSITION = Rotation2d.from_degrees(55)
    LOW_SCORING_POSITION = Rotation2d.from_degrees(110)


class ScoringMechanismProperties:
    EJECT_RING_DISTANCE = 250
