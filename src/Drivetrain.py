import json

from VEXLib.Geometry.Translation1d import Translation1d
from VEXLib.Units import Units
from VEXLib.Math import is_near
from VEXLib.Algorithms.LinearRegressor import LinearRegressor
from VEXLib.Motor import Motor
from VEXLib.Util.Logging import Logger, TimeSeriesLogger
from vex import DEGREES, Brain
from Constants import DrivetrainProperties
from Odometry import TankOdometry
from VEXLib.Algorithms.PID import PIDController
from VEXLib.Algorithms.PIDF import PIDFController
from VEXLib.Algorithms.RateOfChangeCalculator import RateOfChangeCalculator
from VEXLib.Algorithms.TrapezoidProfile import *
from VEXLib.Geometry import GeometryUtil
from VEXLib.Geometry.Pose2d import Pose2d
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Velocity1d import Velocity1d
from VEXLib.Util import ContinuousTimer, time
from VEXLib.Util.motor_tests import collect_power_relationship_data
import VEXLib.Math.MathUtil as MathUtil


drivetrain_log = Logger(Brain().sdcard, Brain().screen, "drivetrain")


class Drivetrain:
    def __init__(self, left_motors: list[Motor], right_motors: list[Motor], inertial_sensor, log_function=print):
        self.left_motors = left_motors
        self.right_motors = right_motors

        self.log = drivetrain_log

        self.odometry = TankOdometry(inertial_sensor)
        self.ANGLE_DIRECTION = 1

        self.left_drivetrain_PID = PIDFController(0.15, 0, 0,  0.576953*1.1, t=1e-5)
        self.right_drivetrain_PID = PIDFController(0.15, 0, 0, 0.5742773*1.1, t=1e-5)

        self.left_speed = 0
        self.right_speed = 0

        self.left_drivetrain_speed_calculator = RateOfChangeCalculator(minimum_sample_time=0.075)
        self.right_drivetrain_speed_calculator = RateOfChangeCalculator(minimum_sample_time=0.075)

        self.position_PID = PIDController(5, 0.1, 0, 0.02, 10)
        self.rotation_PID = PIDController(0.9, 0.0, 0.04, 0.02, 10)

        self.trapezoidal_profile = TrapezoidProfile(
            Constraints(DrivetrainProperties.MAX_ACHIEVABLE_SPEED.to_meters_per_second(),
                        DrivetrainProperties.MAX_ACHIEVABLE_SPEED.to_meters_per_second()))

        self.TURNING_THRESHOLD = DrivetrainProperties.TURNING_THRESHOLD

        self.target_pose = self.odometry.zero_rotation

    def set_angles_inverted(self, inverted):
        self.ANGLE_DIRECTION = -1 if inverted else 1

    def update_odometry(self):
        self.odometry.update(self.get_left_distance(), self.get_right_distance())

    def set_powers(self, left_power, right_power):
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
            self.log.warn("Turn timed out, still",  Units.radians_to_degrees(self.rotation_PID.setpoint - self.odometry.get_rotation().to_radians()), "degrees away")
        self.set_speed_zero_to_one(0, 0)
        self.set_powers(0, 0)
        self.left_drivetrain_PID.reset()
        self.right_drivetrain_PID.reset()

    def move_distance_towards_direction_trap(self, distance: Translation1d, direction_degrees, turn_first=True, turn_correct=True):
        self.log.info("Driving", ("forwards" if distance.to_meters() > 0 else "backwards"), distance.to_centimeters(), "cm at", direction_degrees.to_degrees(), "degrees")
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
                rotation_output = -self.rotation_PID.update(self.odometry.get_rotation().to_radians()) * DrivetrainProperties.TURN_CORRECTION_SCALAR_WHILE_MOVING
            else:
                rotation_output = 0

            self.set_speed_zero_to_one(output_speed + rotation_output, output_speed - rotation_output)
            self.update_powers()
            self.update_odometry()

            at_setpoint = self.position_PID.at_setpoint(DrivetrainProperties.MOVEMENT_DISTANCE_THRESHOLD)
            time_exceeded = elapsed_time >= total_time + DrivetrainProperties.MOVEMENT_MAX_EXTRA_TIME
            if elapsed_time >= total_time and (at_setpoint or time_exceeded):
                self.log.debug("Terminating movement: at_setpoint: ", at_setpoint, "time_exceeded: ", time_exceeded)
                break

        self.log.debug("Remaining Distance: " + str(distance.to_meters() - distance_traveled))
        self.log.debug("Distance Traveled: " + str(distance_traveled))

        self.set_speed_zero_to_one(0, 0)
        self.set_powers(0, 0)
        self.left_drivetrain_PID.reset()
        self.right_drivetrain_PID.reset()
        self.log.trace("Reset drivetrain speed PIDs")

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
        self.odometry.zero_pose = new_zero_pose

    def init(self):
        self.left_drivetrain_PID.reset()
        self.right_drivetrain_PID.reset()

    def set_pose(self):
        self.odometry.pose = Pose2d()
        self.odometry.inertial_sensor.reset_rotation()

    def measure_properties(self):
        self.log.info("Measuring drivetrain properties...")
        collect_power_relationship_data("logs/left_drivetrain.csv", self.left_motors, max_power=0.8)
        self.log.info("Measured left drivetrain properties...")
        collect_power_relationship_data("logs/right_drivetrain.csv", self.right_motors, max_power=0.8)
        self.log.info("Measured right drivetrain properties...")

    def debug(self, imperial=False):
        data = {"time (s)": time.time()}
        if imperial:
            data["left_position (in)"] = self.get_left_distance().to_inches()
            data["right_position (in)"] = self.get_right_distance().to_inches()
            data["left_speed (in/s)"] = self.get_left_speed().to_inches_per_second()
            data["right_speed (in/s)"] = self.get_right_speed().to_inches_per_second()
            data["x position (in)"] = self.odometry.pose.translation.x_component.to_inches()
            data["y position (in)"] = self.odometry.pose.translation.y_component.to_inches()
            data["rotation (deg)"] = self.odometry.pose.rotation.to_degrees()
        else:
            data["left_position (cm)"] = self.get_left_distance().to_centimeters()
            data["right_position (cm)"] = self.get_right_distance().to_centimeters()
            data["raw_left_speed (cm/s)"] = Units.meters_to_centimeters(self.left_drivetrain_speed_calculator.last_rate)
            data["left_speed (cm/s)"] = self.get_left_speed().to_centimeters_per_second()
            data["raw_right_speed (cm/s)"] = Units.meters_to_centimeters(self.right_drivetrain_speed_calculator.last_rate)
            data["right_speed (cm/s)"] = self.get_right_speed().to_centimeters_per_second()
            data["x position (cm)"] = self.odometry.pose.translation.x_component.to_centimeters()
            data["y position (cm)"] = self.odometry.pose.translation.y_component.to_centimeters()
            data["rotation (deg)"] = self.odometry.pose.rotation.to_degrees()
        return data

    def verify_speed_pid(self):
        self.log.info("Initializing time series logger")
        speed_logger = TimeSeriesLogger("logs/speed_pid_data.csv", self.debug().keys())

        self.log.info("Start verifying speed PID")
        self.set_speed(Velocity1d.from_centimeters_per_second(50), Velocity1d.from_centimeters_per_second(50))
        self.log.debug("Setting speeds to +/+50 cm/sec for 3 seconds")
        start_time = time.time()
        while time.time() - start_time < 3:
            self.update_odometry()
            self.update_powers()
            data = self.debug()
            speed_logger.write_data(data)
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
        self.set_speed(Velocity1d.from_centimeters_per_second(0), Velocity1d.from_centimeters_per_second(0))
        self.update_odometry()
        self.set_powers(0, 0)

    def determine_speed_pid_constants(self):
        # Collect power relationship data
        data_json_left = collect_power_relationship_data(self.left_motors, speed_function=lambda motor: ((self.update_drivetrain_velocities(), self.get_speeds())[1][0]).to_meters_per_second())
        data_json_right = collect_power_relationship_data(self.right_motors, speed_function=lambda motor: ((self.update_drivetrain_velocities(), self.get_speeds())[1][1]).to_meters_per_second())
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
        best_error = float('inf')
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

    def verify_odometry(self):
        self.init()
        self.log.info("Initial debug dump: " + str(self.debug()))
        self.log.info("Moving at 0 degrees counterclockwise for 3 seconds at 50 cm/sec")
        self.move_distance_towards_direction_trap(Translation1d.from_meters(0.5), Rotation2d.from_degrees(0))



        self.set_speed(Velocity1d.from_centimeters_per_second(50), Velocity1d.from_centimeters_per_second(50))
        start_time = time.time()
        while time.time() - start_time < 3:
            self.update_odometry()
            self.update_powers()
        self.set_speed_zero_to_one(0, 0)
        while time.time() - start_time < 3.25:
            self.update_odometry()
            self.update_powers()

        final_pose = self.odometry.get_pose()
        final_translation = final_pose.translation

        self.log.info("Should now be at 150cm on X axis")
        self.log.info("Should now be at 0cm on X axis")

        self.log.info("X position ", final_translation.x_component.to_centimeters(), "cm")
        self.log.info("Y position ", final_translation.y_component.to_centimeters(), "cm")

        if not is_near(final_translation.x_component.to_centimeters(), 150, 5):
            self.log.error("The robot did not move to the correct position on the X axis, check the log above")
        if not is_near(final_translation.y_component.to_centimeters(), 0, 5):
            self.log.error("The robot did not move to the correct position on the Y axis, check the log above")

        self.log.info("Done moving forwards", self.debug())

        self.log.info("Turning 90 degrees counterclockwise")
        self.turn_to(Rotation2d.from_degrees(90))
        self.log.info("Initial debug dump: ", self.debug())
        self.log.info("Moving at 90 degrees counterclockwise for 3 seconds at 50 cm/sec")
        self.set_speed(Velocity1d.from_centimeters_per_second(50), Velocity1d.from_centimeters_per_second(50))
        start_time = time.time()
        while time.time() - start_time < 3:
            self.update_odometry()
            self.update_powers()
        self.set_speed_zero_to_one(0, 0)
        while time.time() - start_time < 3.25:
            self.update_odometry()
            self.update_powers()

        final_pose = self.odometry.get_pose()
        final_translation = final_pose.translation

        self.log.info("Should now be at 150cm on X axis")
        self.log.info("Should now be at 150cm on X axis")

        self.log.info("X position:", final_translation.x_component.to_centimeters(), "cm")
        self.log.info("Y position:", final_translation.y_component.to_centimeters(), "cm")

        if not is_near(final_translation.x_component.to_centimeters(), 150, 5):
            self.log.error("The robot did not move to the correct position on the X axis, check the log above")
        if not is_near(final_translation.y_component.to_centimeters(), 150, 5):
            self.log.error("The robot did not move to the correct position on the Y axis, check the log above")
