from VEXLib.Geometry.Translation1d import Translation1d
from vex import FORWARD, VOLT, Inertial, DEGREES, Motor
from Constants import SmartPorts, DrivetrainProperties
from Odometry import TankOdometry
from VEXLib.Algorithms.MovingWindowAverage import MovingWindowAverage
from VEXLib.Algorithms.PID import PIDController
from VEXLib.Algorithms.PIDF import PIDFController
from VEXLib.Algorithms.RateOfChangeCalculator import RateOfChangeCalculator
from VEXLib.Algorithms.TrapezoidProfile import *
from VEXLib.Geometry import GeometryUtil
from VEXLib.Geometry.Pose2d import Pose2d
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Velocity1d import Velocity1d
from VEXLib.Util import ContinuousTimer
from VEXLib.Util.motor_tests import collect_power_relationship_data
import VEXLib.Math.MathUtil as MathUtil


class Drivetrain:
    def __init__(self, left_motors: list[Motor], right_motors: list[Motor]):
        self.left_motors = left_motors
        self.right_motors = right_motors

        self.odometry = TankOdometry(Inertial(SmartPorts.INERTIAL_SENSOR))
        self.ANGLE_DIRECTION = 1

        self.left_drivetrain_PID = PIDFController(5, 0, 0, 5)
        self.right_drivetrain_PID = PIDFController(5, 0, 0, 5)

        self.left_drivetrain_speed_calculator = RateOfChangeCalculator()
        self.right_drivetrain_speed_calculator = RateOfChangeCalculator()

        self.left_drivetrain_speed_smoother = MovingWindowAverage(5)
        self.right_drivetrain_speed_smoother = MovingWindowAverage(5)

        self.position_PID = PIDController(15, 0.1, 0.2, 0.05, 10)
        self.rotation_PID = PIDController(0.85 * 0.9, 0, 0.03, 0.01, 1)

        self.trapezoidal_profile = TrapezoidProfile(
            Constraints(DrivetrainProperties.MAX_ACHIEVABLE_SPEED.to_inches_per_second() / 5,
                        DrivetrainProperties.MAX_ACHIEVABLE_SPEED.to_inches_per_second() / 5))

        self.target_pose = self.odometry.zero_rotation

    def set_angles_inverted(self, inverted):
        self.ANGLE_DIRECTION = -1 if inverted else 1

    def update_odometry(self):
        self.odometry.update(self.get_left_distance(), self.get_right_distance())

    def set_powers(self, left_power, right_power):
        for motor in self.left_motors:
            motor.spin(FORWARD, left_power, VOLT)
        for motor in self.right_motors:
            motor.spin(FORWARD, right_power, VOLT)

    def update_voltages(self):
        self.update_drivetrain_velocities()
        current_left_speed, current_right_speed = self.get_speeds()
        left_controller_output = self.left_drivetrain_PID.update(current_left_speed.to_meters_per_second())
        right_controller_output = self.right_drivetrain_PID.update(current_right_speed.to_meters_per_second())

        self.set_powers(left_controller_output / 12, right_controller_output / 12)

    def update_drivetrain_velocities(self):
        instantaneous_left_speed = self.left_drivetrain_speed_calculator.calculate_rate(
            self.get_left_distance().to_meters(), ContinuousTimer.time())
        instantaneous_right_speed = self.right_drivetrain_speed_calculator.calculate_rate(
            self.get_right_distance().to_meters(), ContinuousTimer.time())

        self.left_drivetrain_speed_smoother.add_value(instantaneous_left_speed)
        self.right_drivetrain_speed_smoother.add_value(instantaneous_right_speed)

    def get_speeds(self):
        left_speed = Velocity1d.from_meters_per_second(self.left_drivetrain_speed_smoother.get_average())
        right_speed = Velocity1d.from_meters_per_second(self.right_drivetrain_speed_smoother.get_average())
        return left_speed, right_speed

    def get_left_distance(self) -> Translation1d:
        motor_rotation_degrees = MathUtil.average_iterable([motor.position(DEGREES) for motor in self.left_motors])

        wheel_rotation = Rotation2d.from_degrees(
            motor_rotation_degrees * DrivetrainProperties.MOTOR_TO_WHEEL_GEAR_RATIO)
        return GeometryUtil.arc_length_from_rotation(DrivetrainProperties.WHEEL_CIRCUMFERENCE, wheel_rotation)

    def get_right_distance(self) -> Translation1d:
        motor_rotation_degrees = MathUtil.average_iterable([motor.position(DEGREES) for motor in self.right_motors])

        wheel_rotation = Rotation2d.from_degrees(
            motor_rotation_degrees * DrivetrainProperties.MOTOR_TO_WHEEL_GEAR_RATIO)
        return GeometryUtil.arc_length_from_rotation(DrivetrainProperties.WHEEL_CIRCUMFERENCE, wheel_rotation)

    def set_speed_zero_to_one(self, left_speed_percent, right_speed_percent):
        self.set_speed(DrivetrainProperties.MAX_ACHIEVABLE_SPEED * left_speed_percent,
                       DrivetrainProperties.MAX_ACHIEVABLE_SPEED * right_speed_percent)

    def set_speed(self, left_speed: Velocity1d, right_speed: Velocity1d):
        self.left_drivetrain_PID.setpoint = left_speed.to_meters_per_second()
        self.right_drivetrain_PID.setpoint = right_speed.to_meters_per_second()

    def turn_to_gyro(self, target_heading_degrees):
        old_target_heading = self.rotation_PID.setpoint
        new_target_heading = Rotation2d.from_degrees(target_heading_degrees * self.ANGLE_DIRECTION).to_radians()
        angular_difference = MathUtil.smallest_angular_difference(old_target_heading, new_target_heading)
        self.rotation_PID.setpoint = self.rotation_PID.setpoint + angular_difference
        self.update_odometry()
        self.rotation_PID.reset()
        self.rotation_PID.update(self.odometry.get_rotation().to_radians())
        while not self.rotation_PID.at_setpoint(threshold=Rotation2d.from_degrees(4).to_radians()):
            output = -self.rotation_PID.update(self.odometry.get_rotation().to_radians())
            self.set_speed_zero_to_one(output, -output)
            self.update_voltages()
            self.update_odometry()
        self.set_speed_zero_to_one(0, 0)
        self.set_powers(0, 0)
        self.left_drivetrain_PID.reset()
        self.right_drivetrain_PID.reset()

    def move_distance_towards_direction_trap(self, distance, direction, ramp_up=True, ramp_down=True, turn_first=True):
        if turn_first:
            self.turn_to_gyro(direction)

        left_start_position = self.get_left_distance().to_inches()
        right_start_position = self.get_right_distance().to_inches()

        if ramp_up:
            initial_state = State(0, 0)
        else:
            initial_state = State(0, self.trapezoidal_profile.constraints.max_velocity * MathUtil.sign(
                distance.to_inches()))

        if ramp_down:
            goal_state = State(distance.to_inches(), 0)
        else:
            goal_state = State(distance.to_inches(),
                               self.trapezoidal_profile.constraints.max_velocity * MathUtil.sign(distance.to_inches()))

        start_time = ContinuousTimer.time()

        self.trapezoidal_profile.calculate(0, initial_state, goal_state)

        total_time = self.trapezoidal_profile.total_time()
        elapsed_time = ContinuousTimer.time() - start_time

        while elapsed_time < total_time:
            elapsed_time = ContinuousTimer.time() - start_time
            target_distance_traveled = self.trapezoidal_profile.calculate(elapsed_time, initial_state, goal_state)

            left_position = self.get_left_distance().to_inches() - left_start_position
            right_position = self.get_right_distance().to_inches() - right_start_position

            distance_traveled = MathUtil.average(left_position, right_position)

            self.position_PID.setpoint = target_distance_traveled.position

            output_speed = self.position_PID.update(distance_traveled)

            rotation_output = -self.rotation_PID.update(self.odometry.get_rotation().to_radians())
            self.set_speed_zero_to_one(output_speed + rotation_output, output_speed - rotation_output)
            self.update_voltages()
            self.update_odometry()

        self.set_speed_zero_to_one(0, 0)
        self.set_powers(0, 0)
        self.left_drivetrain_PID.reset()
        self.right_drivetrain_PID.reset()

    # def move_distance_towards_direction_trap_corrected(self, distance, direction, ramp_up=True, ramp_down=True,
    #                                                    turn_first=True):
    #     delta_target = Translation2d(distance, Translation1d.from_meters(0))
    #     delta_target.rotate_by(Rotation2d.from_degrees(direction))
    #
    #     self.target_pose.translation += delta_target
    #
    #     distance, angle = self.get_distance_and_angle_to_target(self.target_pose.translation)
    #     angle = Rotation2d.from_radians(angle)
    #
    #     self.move_distance_towards_direction_trap(distance, angle.to_degrees(), ramp_up, ramp_down, turn_first)
    #
    # def get_distance_and_angle_to_target(self, target_translation: Translation2d):
    #     delta_translation = target_translation - self.odometry.get_translation()
    #
    #     distance = self.odometry.get_translation().distance(target_translation)
    #
    #     target_angle = math.atan2(delta_translation.y_component.to_meters(),
    #                               delta_translation.x_component.to_meters()) + (math.pi / 2)
    #
    #     return distance, target_angle
    #
    # def move_to_position(self, position):
    #     distance, angle = self.get_distance_and_angle_to_target(position)
    #     self.turn_to_gyro(angle)
    #     self.move_distance_towards_direction_trap(distance, angle)

    def update_zero_pose(self, new_zero_pose):
        self.odometry.zero_rotation = new_zero_pose

    def reset(self):
        self.left_drivetrain_PID.reset()
        self.right_drivetrain_PID.reset()
        self.odometry.pose = Pose2d()
        self.odometry.inertial_sensor.reset_rotation()

    def measure_properties(self):
        # We are yielding the results in a generator fashion instead of printing them directly,
        # this lets the robot send the data wherever it wants and keeps the program responsive throughout collection
        yield "Measuring drivetrain properties..."
        yield "Left drivetrain properties:", collect_power_relationship_data(self.left_motors)
        yield "Right drivetrain properties:", collect_power_relationship_data(self.right_motors)

    def debug(self):
        return {
            "left_position (in)": self.get_left_distance().to_inches(),
            "right_position (in)": self.get_right_distance().to_inches(),
            "left_speed (in/s)": self.get_speeds()[0].to_inches_per_second(),
            "right_speed (in/s)": self.get_speeds()[1].to_inches_per_second(),
            "odometry pose (m,rad)": self.odometry.pose
        }
