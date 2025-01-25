import math
import json
import ConstantsV1
import VEXLib.Math.MathUtil as MathUtil
import VEXLib.Units.Units as Units
from Odometry import TankOdometry
from VEXLib.Algorithms.PID import PIDController
from VEXLib.Algorithms.PIDF import PIDFController
from VEXLib.Algorithms.TrapezoidProfile import *
from VEXLib.Geometry import GeometryUtil
from VEXLib.Geometry.Pose2d import Pose2d
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation1d import Translation1d
from VEXLib.Geometry.Translation2d import Translation2d
from VEXLib.Util import ContinuousTimer
from vex import FORWARD, VOLT, Inertial, TURNS, DEGREES, Motor, PERCENT, PowerUnits, TorqueUnits


class Drivetrain:
    """
        A drivetrain controller for a tank drive base
    """

    def __init__(self, left_motors: list[Motor], right_motors: list[Motor], speed_sample_time_ms=5, speed_smoothing_window=5):
        # Make lists containing the left and right sets of motors
        self.left_motors = left_motors
        self.right_motors = right_motors

        # Initialize the inertial sensor
        self.inertial = Inertial(ConstantsV1.SmartPorts.INERTIAL_SENSOR)

        self.odometry = TankOdometry(self.inertial)
        self.ANGLE_DIRECTION = 1

        self.left_drivetrain_PID = PIDFController(1, 3, 0, 1, 0.01, 12)
        self.right_drivetrain_PID = PIDFController(1, 3, 0, 1, 0.01, 12)

        # Set up the PIDs to control the position and heading of the robot
        self.position_PID = PIDController(7, 0.1, 0.2, 0.01, 10)
        self.rotation_PID = PIDController(0.8, 0, 0.1, 0.01, 0)

        # Speed smoothing
        self.SPEED_SAMPLE_TIME_MS = speed_sample_time_ms
        self.SPEED_SMOOTHING_WINDOW = speed_smoothing_window

        # Initialize the previous positions of the drivetrain to 0
        self.last_left_drivetrain_position = 0
        self.last_right_drivetrain_position = 0
        self.previous_speed_sample_time = ContinuousTimer.time()

        self.previous_left_speeds = [0 for _ in range(5)]
        self.previous_right_speeds = [0 for _ in range(5)]

        # Set the physical properties of the drivetrain
        self.max_achievable_speed = ConstantsV1.DrivetrainProperties.MAX_ACHIEVABLE_SPEED
        self.motor_to_wheel_gear_ratio = ConstantsV1.DrivetrainProperties.MOTOR_TO_WHEEL_GEAR_RATIO
        self.encoder_to_wheel_gear_ratio = ConstantsV1.DrivetrainProperties.ENCODER_TO_WHEEL_GEAR_RATIO
        self.track_width = ConstantsV1.DrivetrainProperties.TRACK_WIDTH
        self.wheel_diameter = ConstantsV1.DrivetrainProperties.WHEEL_DIAMETER
        self.wheel_circumference = ConstantsV1.DrivetrainProperties.WHEEL_CIRCUMFERENCE

        # Initialize a TrapezoidProfile object to define the speed and acceleration profiles of the drivetrain
        self.trapezoidal_profile = TrapezoidProfile(Constraints(30 * self.motor_to_wheel_gear_ratio, 50 * self.motor_to_wheel_gear_ratio))

        # We had to change this:
        self.trapezoidal_profile = TrapezoidProfile(Constraints(30, 50))

        # To this:
        self.trapezoidal_profile = TrapezoidProfile(Constraints(50, 100))

        self.target_pose = Pose2d()

    def set_angles_inverted(self, inverted):
        self.ANGLE_DIRECTION = -1 if inverted else 1

    def update_odometry(self):
        self.odometry.update(self.get_left_position(), self.get_right_position())

    def set_voltage(self, left_voltage, right_voltage):
        for motor in self.left_motors:
            motor.spin(FORWARD, left_voltage, VOLT)
        for motor in self.right_motors:
            motor.spin(FORWARD, right_voltage, VOLT)

    def update_motor_voltages(self):
        current_left_speed, current_right_speed = self.update_drivetrain_velocities()
        left_controller_output = self.left_drivetrain_PID.update(current_left_speed)
        right_controller_output = self.right_drivetrain_PID.update(current_right_speed)

        self.set_voltage(left_controller_output, right_controller_output)

    def update_drivetrain_velocities(self):
        current_time = ContinuousTimer.time()
        dx = (current_time - self.previous_speed_sample_time)
        if dx >= Units.milliseconds_to_seconds(self.SPEED_SAMPLE_TIME_MS):

            current_left_position = MathUtil.average_iterable(
                [motor.position(TURNS) for motor in self.left_motors]) * self.motor_to_wheel_gear_ratio
            current_right_position = MathUtil.average_iterable(
                [motor.position(TURNS) for motor in self.right_motors]) * self.motor_to_wheel_gear_ratio

            left_dy = (current_left_position - self.last_left_drivetrain_position)
            right_dy = (current_right_position - self.last_right_drivetrain_position)

            left_output = left_dy / dx
            right_output = right_dy / dx

            self.previous_left_speeds.append(left_output)
            self.previous_right_speeds.append(right_output)
            self.previous_left_speeds = self.previous_left_speeds[-self.SPEED_SMOOTHING_WINDOW:]
            self.previous_right_speeds = self.previous_right_speeds[-self.SPEED_SMOOTHING_WINDOW:]
            self.last_left_drivetrain_position = current_left_position
            self.last_right_drivetrain_position = current_right_position
            self.previous_speed_sample_time = current_time

        left_average_speed = sum(self.previous_left_speeds) / len(self.previous_left_speeds)
        right_average_speed = sum(self.previous_right_speeds) / len(self.previous_right_speeds)

        return left_average_speed, right_average_speed

    def get_left_position(self):
        position = MathUtil.average_iterable([motor.position(DEGREES) for motor in self.left_motors])

        left_position = Rotation2d.from_degrees(
            position * self.motor_to_wheel_gear_ratio)
        return GeometryUtil.arc_length_from_rotation(self.wheel_circumference, left_position)

    def get_right_position(self):
        position = MathUtil.average_iterable([motor.position(DEGREES) for motor in self.right_motors])

        right_position = Rotation2d.from_degrees(
            position * self.motor_to_wheel_gear_ratio)
        return GeometryUtil.arc_length_from_rotation(self.wheel_circumference, right_position)

    def set_speed_rotations_per_second(self, left_speed, right_speed):
        self.left_drivetrain_PID.setpoint = left_speed
        self.right_drivetrain_PID.setpoint = right_speed

    def set_speed_percent(self, left_speed_percent, right_speed_percent):
        left_speed_percent /= 100
        right_speed_percent /= 100
        self.set_speed_rotations_per_second(left_speed_percent * self.max_achievable_speed.to_rotations_per_second(),
                                            right_speed_percent * self.max_achievable_speed.to_rotations_per_second())

    def turn_to_gyro(self, target_heading_degrees, speed=0.5):
        old_target_heading = self.rotation_PID.setpoint
        new_target_heading = Rotation2d.from_degrees(target_heading_degrees * self.ANGLE_DIRECTION).to_radians()
        angular_difference = MathUtil.smallest_angular_difference(old_target_heading, new_target_heading)
        self.rotation_PID.setpoint += angular_difference
        self.rotation_PID.reset()
        self.rotation_PID.update(self.odometry.get_rotation().to_radians())
        while not self.rotation_PID.at_setpoint(threshold=Rotation2d.from_degrees(4).to_radians()):
            output = -self.rotation_PID.update(self.odometry.get_rotation().to_radians())
            output = MathUtil.clamp(output, -speed, speed)
            self.set_speed_percent(output * 100, -output * 100)
            self.update_motor_voltages()
            self.update_odometry()
        self.set_speed_percent(0, 0)
        self.set_voltage(0, 0)
        self.left_drivetrain_PID.reset()
        self.right_drivetrain_PID.reset()

    def move_distance_towards_direction_trap(self, distance, direction, ramp_up=True, ramp_down=True, turn_first=True):
        if turn_first:
            self.turn_to_gyro(direction)

        left_start_position = self.get_left_position().to_inches()
        right_start_position = self.get_right_position().to_inches()

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

        # Get current time
        start_time = ContinuousTimer.time()

        self.trapezoidal_profile.calculate(0, initial_state, goal_state)

        total_time = self.trapezoidal_profile.total_time()
        elapsed_time = ContinuousTimer.time() - start_time

        while elapsed_time < total_time:
            elapsed_time = ContinuousTimer.time() - start_time
            target_distance_traveled = self.trapezoidal_profile.calculate(elapsed_time, initial_state, goal_state)
            print("TIME: " + str(ContinuousTimer.time() - start_time))
            print("TARGET: " + str(target_distance_traveled))

            left_position = self.get_left_position().to_inches() - left_start_position
            right_position = self.get_right_position().to_inches() - right_start_position

            distance_traveled = MathUtil.average(left_position, right_position)

            self.position_PID.setpoint = target_distance_traveled.position

            output_speed = self.position_PID.update(distance_traveled)

            rotation_output = -self.rotation_PID.update(self.odometry.get_rotation().to_radians())
            rotation_output = MathUtil.clamp(rotation_output, -0.5, 0.5)

            self.set_speed_percent(output_speed + (rotation_output * 100), output_speed - (rotation_output * 100))
            self.update_motor_voltages()
            self.update_odometry()

        self.set_speed_percent(0, 0)
        self.set_voltage(0, 0)
        self.left_drivetrain_PID.reset()
        self.right_drivetrain_PID.reset()

    def move_distance_towards_direction_trap_corrected(self, distance, direction, ramp_up=True, ramp_down=True,
                                                       turn_first=True):
        delta_target = Translation2d(distance, Translation1d.from_meters(0))
        delta_target.rotate_by(Rotation2d.from_degrees(direction))

        self.target_pose.translation += delta_target

        distance, angle = self.get_distance_and_angle_to_target(self.target_pose.translation)
        angle = Rotation2d.from_radians(angle)

        self.move_distance_towards_direction_trap(distance, angle.to_degrees(), ramp_up, ramp_down, turn_first)

    def get_distance_and_angle_to_target(self, target_translation: Translation2d):
        """
        Calculate the distance and angle from the current position to the target position.

        :param target_translation: The target Translation2d to calculate the distance and angle to.
        :return: A tuple containing the distance and angle (in radians).
        """

        # Calculate the difference in position
        delta_translation = target_translation - self.odometry.get_translation()

        # Calculate the distance to the target position
        distance = self.odometry.get_translation().distance(target_translation)

        # Calculate the angle to the target position
        target_angle = math.atan2(delta_translation.y_component.to_meters(), delta_translation.x_component.to_meters()) + (math.pi / 2)

        return distance, target_angle

    def move_to_position(self, position):
        distance, angle = self.get_distance_and_angle_to_target(position)
        self.turn_to_gyro(angle)
        self.move_distance_towards_direction_trap(distance, angle)

    def reset(self):
        self.left_drivetrain_PID.reset()
        self.right_drivetrain_PID.reset()
        self.odometry.pose = Pose2d()
        self.odometry.inertial_sensor.reset_rotation()

    import json

    def ramp_voltage_and_collect_data(self, motor_group, step_delay=0.25, voltage_step=0.1, max_voltage=12):
        """
        Ramp the voltage from 0 to the maximum voltage and collect torque, power, and efficiency data.

        :param step_delay: Time (in seconds) to wait between each voltage step.
        :param voltage_step: Incremental voltage step (in volts).
        :param max_voltage: Maximum allowable voltage (in volts).
        :return: A JSON string with torque-voltage, power-voltage, and efficiency-voltage data.
        """
        data = {
            "voltage": [],
            "torque": [],
            "speed": [],
            "power": [],
            "efficiency": []
        }

        print("Starting voltage ramp and data collection...")

        for voltage in [i * voltage_step for i in range(int(max_voltage / voltage_step) + 1)]:
            # Apply the current voltage to the motors
            [motor.spin(FORWARD, voltage, VOLT) for motor in motor_group]
            total_torque = total_speed = total_power = total_efficiency = 0
            # Wait for the drivetrain to respond
            ContinuousTimer.sleep(step_delay)
            for _ in range(10):
                total_torque += sum([motor.torque(TorqueUnits.NM) for motor in motor_group])
                total_speed += sum([motor.velocity(PERCENT) for motor in motor_group])  # in radians/sec
                total_power += sum([motor.power(PowerUnits.WATT) for motor in motor_group])
                total_efficiency += sum([motor.efficiency(PERCENT) for motor in motor_group])
                ContinuousTimer.sleep(0.1)

            average_torque = total_torque / (10 * len(motor_group))
            average_speed = total_speed / (10 * len(motor_group))
            average_power = total_power / (10 * len(motor_group))
            average_efficiency = total_efficiency / (10 * len(motor_group))

            # Append data to the lists
            data["voltage"].append(voltage)
            data["torque"].append(average_torque)
            data["speed"].append(total_speed / (10 * len(motor_group)))
            data["power"].append(total_power / (10 * len(motor_group)))
            data["efficiency"].append(total_efficiency / (10 * len(motor_group)))

            print("Voltage: {:.2f}V, Speed: {:.2f}%, Torque: {:.2f}Nm, Power: {:.2f}W, Efficiency: {:.2f}".format(
                voltage, total_speed / (10 * len(motor_group)), total_torque / (10 * len(motor_group)), total_power / (10 * len(motor_group)), total_efficiency / (10 * len(motor_group))))

        # Stop the drivetrain
        [motor.spin(FORWARD, 0, VOLT) for motor in motor_group]

        # Convert the data to JSON format
        json_data = json.dumps(data)
        return json_data


