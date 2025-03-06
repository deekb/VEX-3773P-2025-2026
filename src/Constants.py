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
    COLOR_SORT = False
    MEASURE_DRIVETRAIN_PROPERTIES_ON_STARTUP = False
    USE_PIDF_CONTROL = False
    ENABLE_DRIVING = True


class DirkPreferences(DefaultPreferences):
    CONTROL_STYLE = ControlStyles.SPLIT_ARCADE
    CUBIC_FILTER_LINEARITY = 1
    TURN_SPEED = 0.7
    COLOR_SORT = True


class DerekPreferences(DefaultPreferences):
    CONTROL_STYLE = ControlStyles.SPLIT_ARCADE
    CUBIC_FILTER_LINEARITY = 1
    USE_PIDF_CONTROL = True
    ENABLE_DRIVING = False


class AllisonPreferences(DefaultPreferences):
    CONTROL_STYLE = ControlStyles.SPLIT_ARCADE
    CUBIC_FILTER_LINEARITY = 1


class CarterPreferences(DefaultPreferences):
    CONTROL_STYLE = ControlStyles.TANK
    CUBIC_FILTER_LINEARITY = 1


class SmartPorts:
    """Drivetrain"""
    FRONT_LEFT_DRIVETRAIN_MOTOR = Ports.PORT14
    REAR_LOWER_LEFT_DRIVETRAIN_MOTOR = Ports.PORT17
    REAR_UPPER_LEFT_DRIVETRAIN_MOTOR = Ports.PORT12

    FRONT_RIGHT_DRIVETRAIN_MOTOR = Ports.PORT15
    REAR_LOWER_RIGHT_DRIVETRAIN_MOTOR = Ports.PORT16
    REAR_UPPER_RIGHT_DRIVETRAIN_MOTOR = Ports.PORT13

    SCORING_ELEVEN_WATT_MOTOR = Ports.PORT6
    SCORING_FIVE_POINT_FIVE_WATT_MOTOR = Ports.PORT3
    WALL_STAKE_MOTOR = Ports.PORT8

    INERTIAL_SENSOR = Ports.PORT11


class ThreeWirePorts:
    """Scoring Mechanism"""
    brain = Brain()
    MOBILE_GOAL_CLAMP_PISTON = brain.three_wire_port.c
    DOINKER_PISTON = brain.three_wire_port.b


class GearRatios:
    DRIVETRAIN = GearSetting.RATIO_6_1


class DrivetrainProperties:
    TURN_TIMEOUT_SECONDS = 2
    TURNING_THRESHOLD = Rotation2d.from_degrees(2)
    MAX_ACHIEVABLE_SPEED = Velocity1d.from_meters_per_second(1.6)
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
    LOADING_POSITION = Rotation2d.from_degrees(-80)
    UPRIGHT_POSITION = Rotation2d.from_degrees(0)
    HIGH_SCORING_POSITION = Rotation2d.from_degrees(60)
    LOW_SCORING_POSITION = Rotation2d.from_degrees(110)


class ScoringMechanismProperties:
    CALIBRATION_OFFSET = 325

    BLACK_HALF_ROTATION_DISTANCE = 1080
    WHITE_HALF_ROTATION_DISTANCE = 1050

    AVERAGE_HALF_ROTATION = (BLACK_HALF_ROTATION_DISTANCE + WHITE_HALF_ROTATION_DISTANCE) / 2

    HOOK_DISTANCE = 100
    RING_DISTANCE = 50
