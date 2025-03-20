import json

import VEXLib.Math.MathUtil as MathUtil
from Constants import DrivetrainProperties
from Odometry import TankOdometry
from VEXLib.Algorithms.LinearRegressor import LinearRegressor
from VEXLib.Algorithms.PID import PIDController
from VEXLib.Algorithms.PIDF import PIDFController
from VEXLib.Algorithms.RateOfChangeCalculator import RateOfChangeCalculator
from VEXLib.Algorithms.TrapezoidProfile import *
from VEXLib.Geometry import GeometryUtil
from VEXLib.Geometry.Pose2d import Pose2d
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation1d import Translation1d, Distance
from VEXLib.Geometry.Translation2d import Translation2d
from VEXLib.Geometry.Velocity1d import Velocity1d
from VEXLib.Math import is_near
from VEXLib.Motor import Motor
from VEXLib.Units import Units
from VEXLib.Util import ContinuousTimer, time
from VEXLib.Util.Logging import Logger, TimeSeriesLogger
from VEXLib.Util.motor_tests import collect_power_relationship_data
from vex import DEGREES, Brain

drivetrain_log = Logger(Brain().sdcard, Brain().screen, "Drivetrain")


class Drivetrain:
    def __init__(self, left_motors: list[Motor], right_motors: list[Motor], inertial_sensor, log_function=print):
        self.log = drivetrain_log
        self.log.trace("Initializing Drivetrain class")

        self.left_motors = left_motors
        self.right_motors = right_motors

        self.odometry = TankOdometry(inertial_sensor)
        self.log.debug("Odometry initialized with inertial_sensor:", inertial_sensor)

        self.ANGLE_DIRECTION = 1
        self.log.debug("ANGLE_DIRECTION set to", self.ANGLE_DIRECTION)

        self.left_drivetrain_PID = PIDFController(DrivetrainProperties.LEFT_PIDF_GAINS, t=1e-5)
        self.right_drivetrain_PID = PIDFController(DrivetrainProperties.RIGHT_PIDF_GAINS, t=1e-5)

        self.left_speed = 0
        self.right_speed = 0

        self.left_drivetrain_speed_calculator = RateOfChangeCalculator(minimum_sample_time=0.075)
        self.right_drivetrain_speed_calculator = RateOfChangeCalculator(minimum_sample_time=0.075)

        self.position_PID = PIDController(DrivetrainProperties.POSITION_PID_GAINS, 0.02, 10)
        self.rotation_PID = PIDController(DrivetrainProperties.ROTATION_PID_GAINS, 0.02, 10)
        self.log.debug("Position and Rotation PID Controllers initialized with gains")

        self.trapezoidal_profile = TrapezoidProfile(
            Constraints(DrivetrainProperties.MAX_ACHIEVABLE_SPEED.to_meters_per_second(),
                        DrivetrainProperties.MAX_ACHIEVABLE_SPEED.to_meters_per_second()))
        self.log.debug("Trapezoidal profile initialized")

        self.TURNING_THRESHOLD = DrivetrainProperties.TURNING_THRESHOLD
        self.log.debug("Turning threshold set to ", self.TURNING_THRESHOLD)

        self.target_pose = Pose2d(Translation2d(), self.odometry.zero_rotation)
        self.log.debug("Target pose initialized to", self.target_pose)

    def set_angles_inverted(self, inverted):
        self.log.debug("Set angles to inverted: ", inverted)
        self.ANGLE_DIRECTION = -1 if inverted else 1

    def update_odometry(self):
        self.odometry.update(self.get_left_distance(), self.get_right_distance())

    def update_target_translation(self, distance: Translation1d, rotation: Rotation2d):
        self.log.trace("Entering update_target_position")
        self.target_pose.rotation = rotation
        rotation += DrivetrainProperties.ROBOT_RELATIVE_TO_FIELD_RELATIVE_ROTATION
        self.target_pose.translation += Translation2d(distance * rotation.cos(),
                                                      distance * rotation.sin())
        self.log.debug("New target translation: {}".format(self.target_pose))

    def get_distance_and_angle_from_position(self, target_translation: Translation2d):
        self.log.trace("Entering get_distance_and_angle_from_position")
        delta_translation = target_translation - self.target_pose.translation
        return delta_translation.length(), delta_translation.angle() - DrivetrainProperties.ROBOT_RELATIVE_TO_FIELD_RELATIVE_ROTATION

    def set_powers(self, left_power, right_power):
        # self.log.trace("Entering set_powers")
        for motor in self.left_motors:
            motor.set(left_power)
        for motor in self.right_motors:
            motor.set(right_power)

    def update_powers(self):
        self.update_drivetrain_velocities()
        current_left_speed, current_right_speed = self.get_speeds()
        left_controller_output = self.left_drivetrain_PID.update(current_left_speed.to_meters_per_second())
        right_controller_output = self.right_drivetrain_PID.update(current_right_speed.to_meters_per_second())

        self.set_powers(left_controller_output, right_controller_output)

    def update_drivetrain_velocities(self):
        if self.left_drivetrain_speed_calculator.ready_for_sample(ContinuousTimer.time()):
            self.left_speed = self.left_drivetrain_speed_calculator.calculate_rate(
                self.get_left_distance().to_meters(), ContinuousTimer.time())
        if self.right_drivetrain_speed_calculator.ready_for_sample(ContinuousTimer.time()):
            self.right_speed = self.right_drivetrain_speed_calculator.calculate_rate(
                self.get_right_distance().to_meters(), ContinuousTimer.time())

    def get_left_speed(self):
        return Velocity1d.from_meters_per_second(self.left_speed)

    def get_right_speed(self):
        return Velocity1d.from_meters_per_second(self.right_speed)

    def get_speeds(self):
        return self.get_left_speed(), self.get_right_speed()

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

    def set_speed_zero_to_one(self, left_speed, right_speed):
        self.set_speed(DrivetrainProperties.MAX_ACHIEVABLE_SPEED * left_speed,
                       DrivetrainProperties.MAX_ACHIEVABLE_SPEED * right_speed)

    def set_speed(self, left_speed: Velocity1d, right_speed: Velocity1d):
        self.left_drivetrain_PID.setpoint = left_speed.to_meters_per_second()
        self.right_drivetrain_PID.setpoint = right_speed.to_meters_per_second()

    def turn_to(self, rotation: Rotation2d):
        self.log.trace("Entering turn_to")
        self.log.info("Turning to", rotation.to_degrees(), "degrees")

        old_target_heading = self.rotation_PID.setpoint

        new_target_heading = rotation.to_radians() * self.ANGLE_DIRECTION

        self.log.debug("old_target_heading", Units.radians_to_degrees(old_target_heading), "degrees")
        self.log.debug("new_target_heading", Units.radians_to_degrees(new_target_heading), "degrees")

        angular_difference = MathUtil.smallest_angular_difference(old_target_heading, new_target_heading)
        self.log.debug("Optimized angular_difference", Units.radians_to_degrees(angular_difference), "degrees")

        self.rotation_PID.setpoint = self.rotation_PID.setpoint + angular_difference
        self.update_odometry()
        self.rotation_PID.reset()
        self.rotation_PID.update(self.odometry.get_rotation().to_radians())
        start_time = time.time()
        while (not self.rotation_PID.at_setpoint(threshold=self.TURNING_THRESHOLD.to_radians())) and (
                time.time() - start_time < DrivetrainProperties.TURN_TIMEOUT_SECONDS):
            output = MathUtil.clamp(-self.rotation_PID.update(self.odometry.get_rotation().to_radians()), -0.7, 0.7)
            self.set_speed_zero_to_one(output, -output)
            self.update_powers()
            self.update_odometry()
        if not self.rotation_PID.at_setpoint(threshold=self.TURNING_THRESHOLD.to_radians()):
            self.log.warn("Turn timed out, still", Units.radians_to_degrees(
                self.rotation_PID.setpoint - self.odometry.get_rotation().to_radians()), "degrees away")
        self.set_speed_zero_to_one(0, 0)
        self.set_powers(0, 0)
        self.left_drivetrain_PID.reset()
        self.right_drivetrain_PID.reset()

    def move_to_point(self, translation: Translation2d, use_back=False):
        self.log.trace("Entering move_to_point")
        distance, angle = self.get_distance_and_angle_from_position(translation)
        if use_back:
            angle += Rotation2d.from_revolutions(0.5)
            distance = distance.inverse()
        self.move_distance_towards_direction_trap(distance, angle.to_degrees())

    def move_distance_towards_direction_trap(self, distance: Translation1d, direction_degrees, turn_first=True,
                                             turn_correct=True):
        self.log.trace("Entering move_distance_towards_direction_trap")
        self.log.debug("Driving", ("forwards" if distance.to_meters() > 0 else "backwards"), distance.to_centimeters(),
                       "cm at", direction_degrees, "degrees")
        if turn_first:
            self.turn_to(Rotation2d.from_degrees(direction_degrees))

        left_start_position = self.get_left_distance().to_meters()
        right_start_position = self.get_right_distance().to_meters()

        initial_state = State(0, 0)
        goal_state = State(distance.to_meters(), 0)

        start_time = ContinuousTimer.time()

        self.trapezoidal_profile.calculate(0, initial_state, goal_state)

        total_time = self.trapezoidal_profile.total_time()
        elapsed_time = ContinuousTimer.time() - start_time

        distance_traveled = 0

        while True:
            elapsed_time = ContinuousTimer.time() - start_time
            target_distance_traveled = self.trapezoidal_profile.calculate(elapsed_time, initial_state, goal_state)

            left_position = self.get_left_distance().to_meters() - left_start_position
            right_position = self.get_right_distance().to_meters() - right_start_position

            distance_traveled = MathUtil.average(left_position, right_position)

            self.position_PID.setpoint = target_distance_traveled.position

            output_speed = self.position_PID.update(distance_traveled)

            if turn_correct:
                rotation_output = -self.rotation_PID.update(
                    self.odometry.get_rotation().to_radians()) * DrivetrainProperties.TURN_CORRECTION_SCALAR_WHILE_MOVING
            else:
                rotation_output = 0

            self.set_speed_zero_to_one(output_speed + rotation_output, output_speed - rotation_output)
            self.update_powers()
            self.update_odometry()

            at_setpoint = self.position_PID.at_setpoint(DrivetrainProperties.MOVEMENT_DISTANCE_THRESHOLD.to_meters())
            time_exceeded = elapsed_time >= total_time + DrivetrainProperties.MOVEMENT_MAX_EXTRA_TIME
            if elapsed_time >= total_time and (at_setpoint or time_exceeded):
                self.log.debug("Terminating movement: at_setpoint: ", at_setpoint, "time_exceeded: ", time_exceeded)
                if time_exceeded:
                    self.log.warn("time_exceeded")
                break

        self.log.debug("Remaining Distance: " + str(distance.to_meters() - distance_traveled))
        self.log.debug("Distance Traveled: " + str(distance_traveled))

        self.set_speed_zero_to_one(0, 0)
        self.set_powers(0, 0)

        self.update_target_translation(distance, Rotation2d.from_degrees(direction_degrees))

        self.left_drivetrain_PID.reset()
        self.right_drivetrain_PID.reset()

    def update_zero_pose(self, new_zero_pose):
        self.log.trace("Entering update_zero_pose")
        self.odometry.zero_pose = new_zero_pose

    def init(self):
        self.log.debug("Entering init")
        self.left_drivetrain_PID.reset()
        self.right_drivetrain_PID.reset()

    def set_pose(self):
        self.log.trace("Entering set_pose")
        self.odometry.pose = Pose2d()
        self.odometry.inertial_sensor.reset_rotation()

    def measure_properties(self):
        self.log.trace("Entering measure_properties")
        self.log.info("Measuring drivetrain properties...")
        collect_power_relationship_data("logs/left_drivetrain.csv", self.left_motors, step_delay=0.1)
        self.log.info("Measured left drivetrain properties...")
        collect_power_relationship_data("logs/right_drivetrain.csv", self.right_motors, step_delay=0.1)
        self.log.info("Measured right drivetrain properties...")

    def debug(self, imperial=False):
        self.log.trace("Entering debug")
        data = {"time (s)": time.time()}
        data["rotation (deg)"] = self.odometry.pose.rotation.to_degrees()
        if imperial:
            data["left_position (in)"] = self.get_left_distance().to_inches()
            data["right_position (in)"] = self.get_right_distance().to_inches()
            data["left_speed (in/s)"] = self.get_left_speed().to_inches_per_second()
            data["right_speed (in/s)"] = self.get_right_speed().to_inches_per_second()
            data["x position (in)"] = self.odometry.pose.translation.x_component.to_inches()
            data["y position (in)"] = self.odometry.pose.translation.y_component.to_inches()
        else:
            data["left_position (cm)"] = self.get_left_distance().to_centimeters()
            data["right_position (cm)"] = self.get_right_distance().to_centimeters()
            data["left_speed (cm/s)"] = self.get_left_speed().to_centimeters_per_second()
            data["right_speed (cm/s)"] = self.get_right_speed().to_centimeters_per_second()
            data["x position (cm)"] = self.odometry.pose.translation.x_component.to_centimeters()
            data["y position (cm)"] = self.odometry.pose.translation.y_component.to_centimeters()
        return data

    def verify_speed_pid(self):
        self.log.trace("Entering verify_speed_pid")
        self.log.info("Initializing time series logger")
        speed_logger = TimeSeriesLogger("logs/speed_pid_data.csv", self.debug().keys())

        self.log.info("Start verifying speed PID")
        self.set_speed(Velocity1d.from_centimeters_per_second(50), Velocity1d.from_centimeters_per_second(50))
        self.log.debug("Setting speeds to +/+50 cm/sec for 3 seconds")
        start_time = time.time()
        while time.time() - start_time < 3:
            self.update_odometry()
            self.update_powers()
            speed_logger.write_data(self.debug())
        self.log.debug("Setting speeds to -/-50 cm/sec for 3 seconds")
        self.set_speed(Velocity1d.from_centimeters_per_second(-50), Velocity1d.from_centimeters_per_second(-50))
        start_time = time.time()
        while time.time() - start_time < 3:
            self.update_odometry()
            self.update_powers()
            data = self.debug()
            speed_logger.write_data(data)
        self.log.debug("Setting speeds to +/-50 cm/sec for 3 seconds")
        self.set_speed(Velocity1d.from_centimeters_per_second(50), Velocity1d.from_centimeters_per_second(-50))
        start_time = time.time()
        while time.time() - start_time < 3:
            self.update_odometry()
            self.update_powers()
            data = self.debug()
            speed_logger.write_data(data)
        self.log.debug("Setting speeds to +/+160 cm/sec for 3 seconds")
        self.set_speed(Velocity1d.from_centimeters_per_second(160), Velocity1d.from_centimeters_per_second(160))
        start_time = time.time()
        while time.time() - start_time < 3:
            self.update_odometry()
            self.update_powers()
            data = self.debug()
            speed_logger.write_data(data)
        self.set_speed(Velocity1d.from_centimeters_per_second(0), Velocity1d.from_centimeters_per_second(0))
        self.update_odometry()
        self.set_powers(0, 0)

    def determine_speed_pid_constants(self):
        self.log.trace("Entering determine_speed_pid_constants")
        # Collect power relationship data
        data_json_left = collect_power_relationship_data("left_data.csv", self.left_motors, speed_function=lambda motor: (
            (self.update_drivetrain_velocities(), self.get_speeds())[1][0]).to_meters_per_second())
        data_json_right = collect_power_relationship_data("right_data.csv", self.right_motors, speed_function=lambda motor: (
            (self.update_drivetrain_velocities(), self.get_speeds())[1][1]).to_meters_per_second())
        self.log.info(data_json_left)
        self.log.info(data_json_right)
        data_left = json.loads(data_json_left)
        data_right = json.loads(data_json_right)

        # Perform linear regression to find kF
        regressor_left = LinearRegressor().smart_fit(list(zip(data_left["speed"], data_left["input_power"])))
        regressor_right = LinearRegressor().smart_fit(list(zip(data_right["speed"], data_right["input_power"])))

        self.log.info("Left KF value is: " + str(regressor_left.slope))
        self.log.info("Right KF value is: " + str(regressor_right.slope))

        self.log.info("Left slope value is: " + str(regressor_left.slope))
        self.log.info("Right slope value is: " + str(regressor_right.slope))

        self.log.info("Left X-int value is: " + str(regressor_left.x_intercept))
        self.log.info("Right X-int value is: " + str(regressor_right.x_intercept))

        self.log.info("Left Y-int value is: " + str(regressor_left.y_intercept))
        self.log.info("Right Y-int value is: " + str(regressor_right.y_intercept))

        self.log.info("Left KP value is: " + str(regressor_left.slope / 3))
        self.log.info("Right KP value is: " + str(regressor_right.slope / 3))

        # # Determine kP by analyzing the error
        best_kp = 0
        best_error = float("inf")
        for kp in [i / 100 for i in range(101)]:
            total_error = 0
            for i in range(len(data_left["input_power"])):
                target_speed = data_left["speed"][i]
                actual_speed = kp * data_left["input_power"][i] + regressor_left.slope * data_left["input_power"][i]
                error = abs(target_speed - actual_speed)
                total_error += error
            if total_error < best_error:
                best_error = total_error
                best_kp = kp

    def log_translation_discrepancy(self):
        actual_translation = self.odometry.get_translation()
        target_translation = self.target_pose.translation

        translation_discrepancy = actual_translation - target_translation

        if imperial:
            self.log.debug("Target position: X: {} in Y: {} in".format(*target_translation.to_inches()))
            self.log.debug("Actual position: X: {} in Y: {} in".format(*target_translation.to_inches()))
            self.log.debug("ΔX: {} in ΔY: {} in".format(*(translation_discrepancy).to_inches()))
            self.log.debug("Off by: {} in at an angle of {}°".format(translation_discrepancy.length().to_inches(),
                                                                     translation_discrepancy.angle().to_degrees()))
        else:
            self.log.debug("Target position: X: {} cm Y: {} cm".format(*target_translation.to_centimeters()))
            self.log.debug("Actual position: X: {} cm Y: {} cm".format(*actual_translation.to_centimeters()))
            self.log.debug("ΔX: {} cm ΔY: {} cm".format(*(translation_discrepancy).to_centimeters()))
            self.log.debug("Off by: {} cm at an angle of {}°".format(translation_discrepancy.length().to_centimeters(),
                                                                     translation_discrepancy.angle().to_degrees()))

        if translation_discrepancy.x_component > tolerance:
            self.log.error("The robot did not move to the correct position on the X axis, check the log above")
        if translation_discrepancy.y_component > tolerance:
            self.log.error("The robot did not move to the correct position on the Y axis, check the log above")

    def verify_odometry(self, tolerance=Distance.from_centimeters(5), imperial=False):
        self.log.trace("Entering verify_odometry")
        self.init()

        self.log_translation_discrepancy()
        self.log.info("First movement")
        self.move_distance_towards_direction_trap(Translation1d.from_feet(8), 0)
        self.log_translation_discrepancy()
        self.log.info("Second movement")
        self.move_distance_towards_direction_trap(Translation1d.from_meters(0.5), -90)
        self.log_translation_discrepancy()
