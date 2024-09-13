import Constants
from Odometry import TankOdometry
from VEXLib.Algorithms.PID import PIDController
from VEXLib.Algorithms.PIDF import PIDFController
from VEXLib.Algorithms.TrapezoidProfile import *
from VEXLib.Geometry.GeometryUtil import GeometryUtil
from VEXLib.Geometry.Pose2d import Pose2d
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Math.MathUtil import MathUtil
from VEXLib.Units.Units import Units
from VEXLib.Util import time
from vex import Motor, GearSetting, FORWARD, VOLT, Inertial, Rotation, Ports, TURNS, DEGREES


class Drivetrain:
    """
        A drivetrain controller for a tank drive base
    """

    def __init__(self, speed_sample_time_ms=5, speed_smoothing_window=5):
        # Initialize drivetrain motors
        self.front_left_motor = Motor(Constants.SmartPorts.FRONT_LEFT_DRIVETRAIN_MOTOR, GearSetting.RATIO_6_1, True)
        self.middle_left_motor = Motor(Constants.SmartPorts.MIDDLE_LEFT_DRIVETRAIN_MOTOR, GearSetting.RATIO_6_1, True)
        self.rear_left_motor = Motor(Constants.SmartPorts.REAR_LEFT_DRIVETRAIN_MOTOR, GearSetting.RATIO_6_1, True)

        self.front_right_motor = Motor(Constants.SmartPorts.FRONT_RIGHT_DRIVETRAIN_MOTOR, GearSetting.RATIO_6_1, False)
        self.middle_right_motor = Motor(Constants.SmartPorts.MIDDLE_RIGHT_DRIVETRAIN_MOTOR, GearSetting.RATIO_6_1, False)
        self.rear_left_motor = Motor(Constants.SmartPorts.REAR_RIGHT_DRIVETRAIN_MOTOR, GearSetting.RATIO_6_1, False)

        # Make lists containing the left and right sets of motors
        self.left_motors = [self.front_left_motor, self.middle_left_motor, self.rear_left_motor]
        self.right_motors = [self.front_right_motor, self.middle_right_motor, self.rear_left_motor]

        self.left_rotation_sensor = Rotation(Ports.PORT7, True)
        self.right_rotation_sensor = Rotation(Ports.PORT14, False)

        self.left_rotation_sensor.reset_position()
        self.right_rotation_sensor.reset_position()

        # Initialize the inertial sensor
        self.inertial = Inertial(Constants.SmartPorts.INERTIAL_SENSOR)

        self.odometry = TankOdometry(self.left_rotation_sensor, self.right_rotation_sensor, self.inertial)

        # TODO: Tune PIDs
        self.left_drivetrain_PID = PIDFController(0.5, 0, 0, 1, 0.01, 10)
        self.right_drivetrain_PID = PIDFController(0.5, 0, 0, 1, 0.01, 10)

        # Set up the PIDs to control the position and heading of the robot
        self.position_PID = PIDController(10, 2, 0, 0.01, 5)
        self.rotation_PID = PIDController(8, 0, 0.4, 0.01, 0)

        # Initialize a TrapezoidProfile object to define the speed and acceleration profiles of the drivetrain
        self.trapezoidal_profile = TrapezoidProfile(Constraints(50, 30))

        # Speed smoothing
        self.SPEED_SAMPLE_TIME_MS = speed_sample_time_ms
        self.SPEED_SMOOTHING_WINDOW = speed_smoothing_window

        # Initialize the previous positions of the drivetrain to 0
        self.last_left_drivetrain_position = 0
        self.last_right_drivetrain_position = 0
        self.previous_speed_sample_time = time.time()

        self.previous_left_speeds = [0 for _ in range(5)]
        self.previous_right_speeds = [0 for _ in range(5)]

        # Set the physical properties of the drivetrain
        self.max_achievable_speed = Constants.DrivetrainProperties.MAX_ACHIEVABLE_SPEED
        self.motor_to_wheel_gear_ratio = Constants.DrivetrainProperties.MOTOR_TO_WHEEL_GEAR_RATIO
        self.track_width = Constants.DrivetrainProperties.TRACK_WIDTH
        self.wheel_diameter = Constants.DrivetrainProperties.WHEEL_DIAMETER
        self.wheel_circumference = Constants.DrivetrainProperties.WHEEL_CIRCUMFERENCE

        self.target_pose = Pose2d()

    def update_odometry(self):
        self.odometry.update(self.get_left_position(), self.get_right_position())

    # TODO Ensure this doesn't break things
    def set_voltage(self, left_voltage, right_voltage):
        for motor in self.left_motors:
            motor.spin(FORWARD, left_voltage, VOLT)
        for motor in self.right_motors:
            motor.spin(FORWARD, right_voltage, VOLT)

    def update_motor_voltages(self):
        current_left_speed, current_right_speed = self.get_drivetrain_speeds()
        print(Rotation2d.from_revolutions(current_left_speed).to_revolutions())
        left_controller_output = self.left_drivetrain_PID.update(current_left_speed)
        right_controller_output = self.right_drivetrain_PID.update(current_right_speed)

        self.set_voltage(left_controller_output, right_controller_output)

    def get_drivetrain_speeds(self) -> tuple[float, float]:
        current_time = time.time()
        dx = (current_time - self.previous_speed_sample_time)
        if dx >= Units.milliseconds_to_seconds(self.SPEED_SAMPLE_TIME_MS):
            current_left_position = self.left_rotation_sensor.position(TURNS)
            current_right_position = self.right_rotation_sensor.position(TURNS)

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
        left_position = Rotation2d.from_degrees(
            self.left_rotation_sensor.position(DEGREES) * self.motor_to_wheel_gear_ratio)
        return GeometryUtil.distance_circle_rolled(self.wheel_circumference, left_position)

    def get_right_position(self):
        right_position = Rotation2d.from_degrees(
            self.right_rotation_sensor.position(DEGREES) * self.motor_to_wheel_gear_ratio)
        return GeometryUtil.distance_circle_rolled(self.wheel_circumference, right_position)

    def set_speed_rotations_per_second(self, left_speed, right_speed):
        self.left_drivetrain_PID.setpoint = left_speed
        self.right_drivetrain_PID.setpoint = right_speed

    def set_speed_percent(self, left_speed_percent, right_speed_percent):
        left_speed_percent /= 100
        right_speed_percent /= 100
        self.set_speed_rotations_per_second(left_speed_percent * self.max_achievable_speed.to_rotations_per_second(),
                                            right_speed_percent * self.max_achievable_speed.to_rotations_per_second())

    # def move_forward_trapezoidal(self, distance):
    #
    #     # Calculate target position
    #     target_position = distance
    #
    #     initial_state = State(self.get_drivetrain_position(), self.get_drivetrain_speed())
    #     goal_state = State(target_position, 0)
    #
    #     # Get current time
    #     start_time = time.time()
    #
    #     self.trapezoidal_profile.calculate(0, initial_state, goal_state)
    #
    #     total_time = self.trapezoidal_profile.total_time()
    #
    #     while time.time() - start_time < total_time + 1:
    #         target_current_state = self.trapezoidal_profile.calculate(time.time() - start_time, initial_state,
    #                                                                   goal_state)
    #         print("TIME: " + str(time.time() - start_time))
    #         print("TARGET: " + str(target_current_state))
    #
    #         print("ACTUAL" + str(State(self.get_drivetrain_position(), self.get_drivetrain_speed())))
    #         print("ACTUAL" + str(self.current_position.x_component.to_inches()))
    #
    #         self.position_PID.setpoint = target_current_state.position
    #
    #         output_speed = self.position_PID.update(self.current_position.x_component.to_inches())
    #
    #         self.set_speed_rotations_per_second(output_speed, output_speed)
    #         self.update_motor_voltages()
    #         self.update_odometry()
    #         # Delay to control loop frequency
    #         time.sleep(0.01)  # Adjust as necessary

    def turn_to_gyro(self, angle, speed=100):
        self.rotation_PID.setpoint = Rotation2d.from_degrees(angle).to_revolutions()
        self.rotation_PID.reset()
        self.rotation_PID.update(self.odometry.get_rotation().to_revolutions())
        while not self.rotation_PID.at_setpoint(threshold=Rotation2d.from_degrees(2).to_revolutions()):
            output = self.rotation_PID.update(self.odometry.get_rotation().to_revolutions())
            self.set_speed_percent(output * speed, -output * speed)
            self.update_motor_voltages()
            self.update_odometry()

    def turn_norm_gyro(self, angle, speed=100):
        angle = (Rotation2d.from_degrees(angle) - self.odometry.get_rotation().to_revolutions()).normalize()
        self.turn_to_gyro(angle.to_degrees())

    def turn_by_angle(self, angle_degrees):
        target_rotation = self.odometry.get_rotation() + Rotation2d.from_degrees(angle_degrees)

        self.rotation_PID.setpoint = target_rotation.to_radians()
        self.rotation_PID.update(self.odometry.get_rotation().to_revolutions())

        while True:
            turning_output = self.rotation_PID.update(self.odometry.get_rotation().to_radians())
            if abs(turning_output) < 0.01:
                break

            self.set_speed_percent(-turning_output, turning_output)
            self.update_motor_voltages()
            self.update_odometry()
            time.sleep(0.01)  # Adjust as necessary
