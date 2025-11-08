import math

from VEXLib.Algorithms.PID import PIDController
from VEXLib.Algorithms.RateOfChangeCalculator import RateOfChangeCalculator
from VEXLib.Geometry.GeometryUtil import arc_length_from_rotation
from VEXLib.Geometry.Pose2d import Pose2d
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation1d import Translation1d
from VEXLib.Geometry.Translation2d import Translation2d
from VEXLib.Geometry.Velocity1d import Velocity1d
from VEXLib.Math import MathUtil
from VEXLib.Util import time
from vex import DEGREES, Inertial, TurnType, FORWARD, VOLT, TURNS, Motor


def desaturate_wheel_speeds(speeds):
    maximum_power = max(*speeds)

    if maximum_power > 1:
        # At least one of the motor velocities are over the maximum possible velocity
        # This will result in clipping, meaning that the motor speeds will be "clipped" off to the maximum (1)
        # We will lose some control of our turning while we are moving quickly
        # To solve this issue we can detect if any motor velocities exceed the maximum possible velocity and
        # Use the inverse of the maximum motor power as a scalar by dividing by it.
        # This will always output all values in a range from 0-1
        speeds = [speed / maximum_power for speed in speeds]
    return speeds


class GenericWheel:
    """
    Represents a wheel in the drivetrain with its motor, direction, speed controller, and wheel circumference.
    """

    def __init__(
        self,
        motor: Motor,
        direction,
        speed_controller: PIDController,
        wheel_circumference,
        motor_to_wheel_gear_ratio,
    ):
        """
        Initializes the GenericWheel.

        Args:
            motor (Motor): The motor controlling the wheel.
            direction (Rotation2d): The direction of the wheel.
            speed_controller (PIDController): The PID controller for the wheel speed.
            wheel_circumference (Translation1d): The circumference of the wheel.
        """
        self.direction: Rotation2d = direction
        self.wheel_circumference = wheel_circumference
        self.motor_to_wheel_gear_ratio = motor_to_wheel_gear_ratio
        self.speed_controller = speed_controller
        self.motor = motor
        self.speed_calculator = RateOfChangeCalculator(minimum_sample_time=0.075)

    def wheel_contribution_coefficient(self, movement_angle_rad: float) -> float:
        """
        Calculates the contribution coefficient of the wheel based on the movement angle.

        Args:
            movement_angle_rad (float): The movement angle in radians.

        Returns:
            float: A coefficient from -1 to 1 representing the correlation of the wheel's movement to the chassis movement in the desired direction.
        """
        return math.cos(self.direction - movement_angle_rad)

    def get_wheel_speed(self) -> Velocity1d:
        """
        Gets the current speed of the wheel.

        Returns:
            Velocity1d: The current speed of the wheel.
        """
        return Velocity1d.from_meters_per_second(
            self.speed_calculator.calculate_rate(
                arc_length_from_rotation(
                    self.wheel_circumference,
                    Rotation2d.from_revolutions(self.motor.position(TURNS))
                    * self.motor_to_wheel_gear_ratio,
                ).to_meters(),
                time.time(),
            )
        )

    def set_target_wheel_velocity(self, velocity: Velocity1d):
        """
        Sets the target velocity for the wheel.

        Args:
            velocity (Velocity1d): The target velocity.
        """
        self.speed_controller.setpoint = velocity.to_meters_per_second()

    def update(self):
        """
        Updates the controller output based on the wheel's current speed.
        """
        self.motor.spin(
            FORWARD,
            self.speed_controller.update(self.get_wheel_speed().to_meters_per_second()),
            VOLT,
        )

    def calculate_desired_wheel_speed(
        self, movement_angle: Rotation2d, movement_speed: Velocity1d
    ):
        """
        Calculates the wheel speed based on the movement angle and speed.

        Args:
            movement_angle (Rotation2d): The movement angle.
            movement_speed (Velocity1d): The movement speed.

        Returns:
            float: The calculated wheel speed.
        """
        return movement_speed * self.wheel_contribution_coefficient(
            movement_angle.to_radians()
        )


class GenericDrivetrain:
    """
    Represents a generic drivetrain with multiple wheels and an inertial sensor.
    """

    def __init__(self, inertial_sensor, wheels: list[GenericWheel]):
        """
        Initializes the GenericDrivetrain.

        Args:
            inertial_sensor (Inertial): The inertial sensor for the drivetrain.
            wheels (list[GenericWheel]): The list of wheels in the drivetrain.
        """
        self.wheels = wheels
        self.odometry = GenericOdometry(inertial_sensor, self.wheels)

    def move(self, movement_angle: Rotation2d, movement_speed: Velocity1d):
        """
        Moves the drivetrain based on the movement angle and speed.

        Args:
            movement_angle (Rotation2d): The movement angle.
            movement_speed (Velocity1d): The movement speed.
        """
        wheel_speeds = []
        for wheel in self.wheels:
            wheel.set_target_wheel_velocity(
                wheel.wheel_speed(movement_angle, movement_speed)
            )

        return wheel_speeds


class GenericOdometry:
    """
    A class that manages odometry for any drivetrain. This system calculates
    the robot's pose (position and rotation) on a 2D plane using sensor inputs and geometric calculations.
    """

    def __init__(self, inertial_sensor: Inertial, wheel_directions: list):
        """
        Initializes the GenericOdometry system.

        Args:
            inertial_sensor (Inertial): The inertial sensor used for rotation measurements.
            wheel_directions (list): The directions of the wheels.
        """
        # Device to measure the robot's rotational orientation
        self.inertial_sensor = inertial_sensor
        self.inertial_sensor.set_turn_type(TurnType.LEFT)

        # Tracks the last recorded wheel positions
        self.last_wheel_positions = []

        # Stores the current pose of the robot (position and orientation)
        self.pose = Pose2d()

        # Rotation offset to align the inertial sensor's initial orientation with the robot's coordinate system
        self.zero_rotation = Rotation2d()

        # Directions of the wheels
        self.wheel_directions = wheel_directions

    def update(self, wheel_positions: list):
        """
        Updates the robot's odometry based on new wheel positions.

        Args:
            wheel_positions (list): The current positions of the wheels.
        """
        if not self.last_wheel_positions:
            self.last_wheel_positions = wheel_positions
            return

        if len(wheel_positions) != len(self.wheel_directions):
            raise ValueError(
                "Length mismatch between wheel_positions and self.wheel_directions"
            )

        # Calculate distances traveled by each wheel since the last update
        distances = [
            current - last
            for current, last in zip(wheel_positions, self.last_wheel_positions)
        ]

        # Update last wheel positions to current positions
        self.last_wheel_positions = wheel_positions

        wheel_distances_and_directions = list(zip(distances, self.wheel_directions))

        # Calculate the weights based on the cosine of the wheel directions
        y_distance = Translation1d.from_meters(
            MathUtil.average_iterable(
                [
                    direction.sin() * distance.to_meters()
                    for distance, direction in wheel_distances_and_directions
                ]
            )
        )
        x_distance = Translation1d.from_meters(
            MathUtil.average_iterable(
                [
                    direction.cos() * distance.to_meters()
                    for distance, direction in wheel_distances_and_directions
                ]
            )
        )

        robot_relative_translation = Translation2d(x_distance, y_distance)

        self.pose.rotation = (
            Rotation2d.from_degrees(self.inertial_sensor.rotation(DEGREES))
            - self.zero_rotation
        )

        # Update the robot's 2D position based on forward distance and orientation
        self.pose.translation = (
            self.pose.translation
            + robot_relative_translation.rotate_by(self.pose.rotation)
        )

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
