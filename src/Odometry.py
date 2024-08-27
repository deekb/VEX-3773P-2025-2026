import math

from VEXLib.Geometry.GeometryUtil import GeometryUtil
from VEXLib.Geometry.Pose2d import Pose2d
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Math.MathUtil import MathUtil
from VEXLib.Util import time
from vex import DEGREES


class TankOdometry:
    def __init__(self, left_motors, right_motors, track_width, wheel_circumference, motor_to_wheel_gear_ratio):
        # Constants
        self.WHEEL_CIRCUMFERENCE = wheel_circumference
        self.MOTOR_TO_WHEEL_GEAR_RATIO = motor_to_wheel_gear_ratio
        self.TRACK_WIDTH = track_width
        self.TURN_CIRCUMFERENCE = self.TRACK_WIDTH * math.pi

        # State variables
        self.left_motors = left_motors
        self.right_motors = right_motors

        self.last_left_position = self.get_left_position()
        self.last_right_position = self.get_right_position()
        self.last_time = time.time()
        self.pose = Pose2d()

    def get_left_position(self):
        positions = [motor.position(DEGREES) for motor in self.left_motors]
        average_position = MathUtil.average_iterable(positions)
        average_position = Rotation2d.from_degrees(average_position)
        return GeometryUtil.distance_circle_rolled(self.WHEEL_CIRCUMFERENCE, average_position) * self.MOTOR_TO_WHEEL_GEAR_RATIO

    def get_right_position(self):
        average_position = Rotation2d.from_degrees(MathUtil.average_iterable([motor.position(DEGREES) for motor in self.left_motors]))
        return GeometryUtil.distance_circle_rolled(self.WHEEL_CIRCUMFERENCE, average_position) * self.MOTOR_TO_WHEEL_GEAR_RATIO

    def update(self):
        left_position = self.get_left_position()
        right_position = self.get_right_position()

        left_distance = left_position - self.last_left_position
        right_distance = right_position - self.last_right_position
        self.last_left_position = left_position
        self.last_right_position = right_position

        forward_distance = MathUtil.average(left_distance, right_distance)

        delta_rotation = (right_distance - left_distance) / self.TRACK_WIDTH

        self.pose.rotation += delta_rotation
        #
        # self.pose.translation += Translation2d(forward_distance * delta_rotation.cos(),
        #                                        forward_distance * delta_rotation.sin())

    def get_pose(self):
        return self.pose

    def get_translation(self):
        return self.pose.translation

    def get_rotation(self):
        return self.pose.rotation

    def send_telemetry(self, telemetry):
        telemetry.send_message("Odometry Translation (meters): " + str(self.get_translation()) + ", Rotation (degrees): " + str(self.get_rotation().to_degrees()))
