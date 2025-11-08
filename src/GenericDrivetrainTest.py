import VEXLib.Util.time as time
from VEXLib.Algorithms.PIDF import PIDFController
from VEXLib.Algorithms.RateOfChangeCalculator import RateOfChangeCalculator
from VEXLib.Geometry.GeometryUtil import arc_length_from_rotation, circle_circumference
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation1d import Distance
from VEXLib.Geometry.Velocity1d import Velocity1d
from VEXLib.Kinematics import GenericDrivetrain, GenericWheel
from VEXLib.Robot.RobotBase import RobotBase
from vex import Inertial, Ports, Motor, TURNS


class PIDGains:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd


class PIDFGains(PIDGains):
    def __init__(self, kp, ki, kd, kf=0.0):
        super().__init__(kp, ki, kd)
        self.kf = kf


class DrivetrainProperties:
    # PID gains
    LEFT_PIDF_GAINS = PIDFGains(0.2, 0, 0, 0.6)
    RIGHT_PIDF_GAINS = PIDFGains(0.2, 0, 0, 0.6)

    POSITION_PID_GAINS = PIDGains(5, 1, 0)
    ROTATION_PID_GAINS = PIDGains(0.75, 0.0, 0.02)

    ROBOT_RELATIVE_TO_FIELD_RELATIVE_ROTATION = Rotation2d.from_degrees(90)
    TURN_TIMEOUT_SECONDS = 2
    TURN_CORRECTION_SCALAR_WHILE_MOVING = 0.9
    TURNING_THRESHOLD = Rotation2d.from_degrees(3)
    MOVEMENT_DISTANCE_THRESHOLD = Distance.from_centimeters(0.5)
    MOVEMENT_MAX_EXTRA_TIME = 1
    MAX_ACHIEVABLE_SPEED = Velocity1d.from_meters_per_second(1.6)
    MOTOR_TO_WHEEL_GEAR_RATIO = 36 / 60
    WHEEL_DIAMETER = Distance.from_inches(3.235)
    WHEEL_CIRCUMFERENCE = circle_circumference(WHEEL_DIAMETER / 2)


class Robot(RobotBase):
    def __init__(self, brain):
        super().__init__(brain)

        self.inertial_sensor = Inertial(Ports.PORT1)

        self.left_speed_calculator = RateOfChangeCalculator(minimum_sample_time=0.075)
        self.right_speed_calculator = RateOfChangeCalculator(minimum_sample_time=0.075)

        self.drivetrain = GenericDrivetrain(
            self.inertial_sensor,
            [
                GenericWheel(
                    Motor(Ports.PORT2),
                    Rotation2d.from_degrees(0),
                    lambda: self.left_speed_calculator.calculate_rate(
                        arc_length_from_rotation(
                            DrivetrainProperties.WHEEL_CIRCUMFERENCE,
                            Rotation2d.from_revolutions(
                                Motor(Ports.PORT2).position(TURNS)
                            ),
                        ).to_meters(),
                        time.time(),
                    ),
                    PIDFController(DrivetrainProperties.LEFT_PIDF_GAINS),
                )
            ],
        )
