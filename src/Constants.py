from VEXLib.Geometry.GeometryUtil import circle_circumference
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation1d import Distance
from VEXLib.Geometry.Velocity1d import Velocity1d
from CornerMechanism import Sides
from vex import Ports, GearSetting, Brain


class PIDGains:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd


class PIDFGains(PIDGains):
    def __init__(self, kp, ki, kd, kf=0.0):
        super().__init__(kp, ki, kd)
        self.kf = kf


class ControlStyles:
    TANK = 1
    ARCADE = 2
    SPLIT_ARCADE = 3


class DefaultPreferences:
    CONTROL_STYLE = ControlStyles.TANK
    CUBIC_FILTER_LINEARITY = 1
    MOVE_SPEED = 1
    TURN_SPEED = 1
    DO_TURN_DECAY = False
    COLOR_SORT = False
    MEASURE_DRIVETRAIN_PROPERTIES_ON_STARTUP = False
    USE_PIDF_CONTROL = False
    PIDF_GAINS = PIDFGains(0, 0, 0, 0.6)
    ENABLE_DRIVING = True
    CORNER_MECHANISM_DRIVER = Sides.RIGHT


class DirkPreferences(DefaultPreferences):
    CONTROL_STYLE = ControlStyles.SPLIT_ARCADE
    CUBIC_FILTER_LINEARITY = 1
    DO_TURN_DECAY = True
    TURN_SPEED = 0.7
    COLOR_SORT = True


class DirkPreferencesNoColorSort(DirkPreferences):
    COLOR_SORT = False


class DerekPreferences(DefaultPreferences):
    CONTROL_STYLE = ControlStyles.SPLIT_ARCADE
    CUBIC_FILTER_LINEARITY = 0.7
    USE_PIDF_CONTROL = True
    PIDF_GAINS = PIDFGains(0.1, 0, 0, 0.6)
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
    RING_DESCORER_PISTON = brain.three_wire_port.a
    LEFT_DOINKER_PISTON = brain.three_wire_port.b
    RIGHT_DOINKER_PISTON = brain.three_wire_port.d
    RING_RUSH_MECHANISM_PISTON = brain.three_wire_port.e


class GearRatios:
    DRIVETRAIN = GearSetting.RATIO_6_1


class DrivetrainProperties:
    # PID gains
    LEFT_PIDF_GAINS = PIDFGains(0.2, 0, 0, 0.6)
    RIGHT_PIDF_GAINS = PIDFGains(0.2, 0, 0, 0.6)

    POSITION_PID_GAINS = PIDGains(5, 0, 0)
    ROTATION_PID_GAINS = PIDGains(0.8, 0.0, 0.03)

    ROBOT_RELATIVE_TO_FIELD_RELATIVE_ROTATION = Rotation2d.from_degrees(90)
    TURN_TIMEOUT_SECONDS = 2
    TURN_CORRECTION_SCALAR_WHILE_MOVING = 0.9
    TURNING_THRESHOLD = Rotation2d.from_degrees(3)
    MOVEMENT_DISTANCE_THRESHOLD = Distance.from_centimeters(1)
    MOVEMENT_MAX_EXTRA_TIME = 1
    MAX_ACHIEVABLE_SPEED = Velocity1d.from_meters_per_second(1.6)
    MOTOR_TO_WHEEL_GEAR_RATIO = (36 / 60)
    WHEEL_DIAMETER = Distance.from_inches(3.235)
    WHEEL_CIRCUMFERENCE = circle_circumference(WHEEL_DIAMETER / 2)


class WallStakeMechanismProperties:
    PID_GAINS = PIDGains(kp=50, ki=0, kd=1)
    FEEDFORWARD_GAIN = 0.9
    DOCKED_POSITION = Rotation2d.from_degrees(-100)
    POSITIONAL_TOLERANCE = Rotation2d.from_degrees(2)
    LOADING_POSITION = Rotation2d.from_degrees(-80)
    UPRIGHT_POSITION = Rotation2d.from_degrees(0)
    HIGH_SCORING_POSITION = Rotation2d.from_degrees(60)
    LOW_SCORING_POSITION = Rotation2d.from_degrees(110)


class ScoringMechanismProperties:

    BLACK_HALF_ROTATION_DISTANCE = 1080
    WHITE_HALF_ROTATION_DISTANCE = 1050

    FULL_HOOK_ROTATION_DEGREES = 2128.939

    AVERAGE_HALF_ROTATION = (WHITE_HALF_ROTATION_DISTANCE + BLACK_HALF_ROTATION_DISTANCE) / 2
    CALIBRATION_OFFSET = 220

    HOOK_DISTANCE = 100
    RING_DISTANCE = 50
