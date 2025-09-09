from VEXLib.Geometry.GeometryUtil import circle_circumference
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation1d import Distance
from VEXLib.Geometry.Velocity1d import Velocity1d
from VEXLib.Sensors.Controller import ControlStyles
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


class DefaultPreferences:
    CONTROL_STYLE = ControlStyles.TANK
    CUBIC_FILTER_LINEARITY = 1.0
    MOVE_SPEED = 1.0
    TURN_SPEED = 1.0
    DO_TURN_DECAY = False
    USE_PIDF_CONTROL = False
    PIDF_GAINS = PIDFGains(0.2, 0, 0, 0.6)
    ENABLE_DRIVING = True
    INPUT_DEBUG_MODE = False


class ColtonPreferences(DefaultPreferences):
    CONTROL_STYLE = ControlStyles.SPLIT_ARCADE
    CUBIC_FILTER_LINEARITY = 1
    USE_PIDF_CONTROL = True


class SmartPorts:
    """Drivetrain"""

    FRONT_LEFT_DRIVETRAIN_MOTOR = Ports.PORT20
    REAR_LOWER_LEFT_DRIVETRAIN_MOTOR = Ports.PORT19
    REAR_UPPER_LEFT_DRIVETRAIN_MOTOR = Ports.PORT18

    FRONT_RIGHT_DRIVETRAIN_MOTOR = Ports.PORT13
    REAR_LOWER_RIGHT_DRIVETRAIN_MOTOR = Ports.PORT12
    REAR_UPPER_RIGHT_DRIVETRAIN_MOTOR = Ports.PORT11

    LOWER_ROLLER_MOTOR = Ports.PORT7
    UPPER_ROLLER_MOTOR = Ports.PORT3
    BUCKET_ROLLER_MOTOR = Ports.PORT5

    INERTIAL_SENSOR = Ports.PORT1


class ThreeWirePorts:
    """Scoring Mechanism"""

    brain = Brain()
    # PISTON = brain.three_wire_port.e


class GearRatios:
    DRIVETRAIN = GearSetting.RATIO_6_1
    LOWER_ROLLER = GearSetting.RATIO_18_1
    UPPER_ROLLER = GearSetting.RATIO_18_1
    BUCKET_ROLLER = GearSetting.RATIO_18_1


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
    MOTOR_TO_WHEEL_GEAR_RATIO = 36 / 60
    WHEEL_DIAMETER = Distance.from_inches(3.235)
    WHEEL_CIRCUMFERENCE = circle_circumference(WHEEL_DIAMETER / 2)
