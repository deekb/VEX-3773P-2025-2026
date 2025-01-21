from VEXLib.Geometry.Pose2d import Pose2d
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation1d import Distance, Translation1d
from VEXLib.Geometry.Translation2d import Translation2d
import VEXLib.Math.MathUtil as MathUtil
from vex import DEGREES, Inertial


class TankOdometry:
    """
    A class that manages odometry for a tank drive robot. This system calculates
    the robot's pose (position and rotation) on a 2D plane using sensor inputs and geometric calculations.
    """

    def __init__(self, inertial_sensor: Inertial):
        """
        Initializes the TankOdometry system.

        Args:
            inertial_sensor (Inertial): The inertial sensor used for rotation measurements.
        """
        # Device to measure the robot's rotational orientation
        self.inertial_sensor = inertial_sensor

        # Tracks the last recorded left and right wheel positions
        self.last_left_position = Distance()
        self.last_right_position = Distance()

        # Stores the current pose of the robot (position and orientation)
        self.pose = Pose2d()

        # Rotation offset to align the inertial sensor's initial orientation with the robot's coordinate system
        self.starting_offset = Rotation2d()

    def update(self, left_rotation: Translation1d, right_rotation: Translation1d):
        """
        Updates the robot's odometry based on new left and right wheel positions.

        Args:
            left_rotation (Distance): The current rotation of the left wheel.
            right_rotation (Distance): The current rotation of the right wheel.
        """
        # Calculate distance traveled by each wheel since the last update
        left_distance = left_rotation - self.last_left_position
        right_distance = right_rotation - self.last_right_position

        # Update last wheel positions to current positions
        self.last_left_position = left_rotation
        self.last_right_position = right_rotation

        # Calculate the average forward distance traveled by the two sides of the robot
        forward_distance = Distance.from_meters(
            MathUtil.average(left_distance.to_meters(), right_distance.to_meters())
        )

        # Update the robot's rotational orientation using the inertial sensor
        self.pose.rotation = Rotation2d.from_degrees(
            -self.inertial_sensor.rotation(DEGREES) + self.starting_offset.to_degrees()
        )

        # Update the robot's 2D position based on forward distance and orientation
        self.pose.translation += Translation2d(
            forward_distance * self.pose.rotation.cos(),
            forward_distance * self.pose.rotation.sin()
        )

    def get_pose(self) -> Pose2d:
        """
        Returns the robot's current pose, which includes its position and orientation.

        Returns:
            Pose2d: The current pose of the robot.
        """
        return self.pose

    def get_translation(self) -> Translation2d:
        """
        Returns the robot's current translation (2D position).

        Returns:
            Translation2d: The current translation of the robot.
        """
        return self.pose.translation

    def get_rotation(self) -> Rotation2d:
        """
        Returns the robot's current rotation (orientation).

        Returns:
            Rotation2d: The current rotation of the robot.
        """
        return self.pose.rotation
