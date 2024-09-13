import math

from VEXLib.Geometry.GeometryUtil import GeometryUtil
from VEXLib.Geometry.Pose2d import Pose2d
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation1d import Distance
from VEXLib.Geometry.Translation2d import Translation2d
from VEXLib.Math.MathUtil import MathUtil
from VEXLib.Util import time
from vex import DEGREES, Inertial


class TankOdometry:
    def __init__(self, left_rotation_sensor, right_rotation_sensor, inertial_sensor):
        # Devices
        self.left_rotation_sensor = left_rotation_sensor
        self.right_rotation_sensor = right_rotation_sensor
        self.inertial_sensor = inertial_sensor

        # State variables
        self.last_left_position = Distance()
        self.last_right_position = Distance()
        self.last_time = time.time()
        self.pose = Pose2d()

    def update(self, left_position, right_position):
        left_distance = left_position - self.last_left_position
        right_distance = right_position - self.last_right_position
        self.last_left_position = left_position
        self.last_right_position = right_position

        forward_distance = Distance.from_meters(MathUtil.average(left_distance.to_meters(), right_distance.to_meters()))

        self.pose.rotation = Rotation2d.from_degrees(-self.inertial_sensor.heading(DEGREES))

        self.pose.translation += Translation2d(forward_distance * self.pose.rotation.cos(),
                                               forward_distance * self.pose.rotation.sin())

    def get_pose(self):
        return self.pose

    def get_translation(self):
        return self.pose.translation

    def get_rotation(self):
        return self.pose.rotation
