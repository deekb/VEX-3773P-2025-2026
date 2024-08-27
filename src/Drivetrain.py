from VEXLib.Algorithms.PIDF import PIDFController
from VEXLib.Algorithms.PID import PIDController
from VEXLib.Geometry.Translation2d import Translation2d
from VEXLib.Geometry.Translation1d import Distance
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Algorithms.TrapezoidProfile import *
from VEXLib.Math.MathUtil import MathUtil
from VEXLib.Units.Units import Units
from VEXLib.Util import time
import Constants
import math
import sys
from vex import Motor, GearSetting, FORWARD, VOLT, DEGREES, Inertial, Rotation, Ports, TURNS


CLOCKWISE = 1
COUNTERCLOCKWISE = 2


class Drivetrain:
    """
        A drivetrain controller for a tank drive base
    """
    def __init__(self, speed_sample_time_ms=5, speed_smoothing_window=5):
        self.SPEED_SAMPLE_TIME_MS = speed_sample_time_ms
        self.SPEED_SMOOTHING_WINDOW = speed_smoothing_window

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

        # Set up the PIDs to control each side of the drivetrain
        # self.left_drivetrain_PID = PIDFController(0.2, 0.15, 0.0, 0.175, 0.01, 6)
        # self.right_drivetrain_PID = PIDFController(0.2, 0.15, 0.0, 0.175, 0.01, 6)

        self.left_drivetrain_PID = PIDFController(1, 0, 0, 1, 0.01, 0)
        self.right_drivetrain_PID = PIDFController(1, 0, 0, 1, 0.01, 0)

        # Set up the PIDs to control the position and heading of the robot
        self.position_PID = PIDController(10, 2, 0, 0.01, 5)
        self.rotation_PID = PIDController(8, 0, 0.4, 0.01, 0)

        # Initialize a TrapezoidProfile object to define the speed and acceleration profiles of the drivetrain
        self.trapezoidal_profile = TrapezoidProfile(Constraints(50, 30))

        """Odometry"""

        # Initialize the previous positions of the drivetrain to 0
        self.last_left_drivetrain_position_for_odometry = 0
        self.last_right_drivetrain_position_for_odometry = 0
        self.last_left_drivetrain_position_for_speed = 0
        self.last_right_drivetrain_position_for_speed = 0
        self.previous_speed_sample_time = time.time()

        self.previous_left_speeds = [0 for _ in range(5)]
        self.previous_right_speeds = [0 for _ in range(5)]

        # Set the physical properties of the drivetrain
        self.max_achievable_speed_in_rotations_per_second = 11.15
        self.motor_to_wheel_gear_ratio = 36 / 60
        self.track_width_in_inches = 13.5
        self.wheel_diameter_in_inches = 3.22772
        self.wheel_circumference_in_inches = self.wheel_diameter_in_inches * math.pi

        self.target_position = Translation2d()
        self.target_rotation = Rotation2d()

        self.current_position = Translation2d()
        self.current_rotation = Rotation2d()

    def set_voltage(self, left_voltage, right_voltage):
        for motor in self.left_motors:
            motor.spin(FORWARD, left_voltage, VOLT)
        for motor in self.right_motors:
            motor.spin(FORWARD, right_voltage, VOLT)

    def get_drivetrain_speeds(self) -> tuple[float, float]:
        current_time = time.time()
        dx = (current_time - self.previous_speed_sample_time)
        if dx >= Units.milliseconds_to_seconds(self.SPEED_SAMPLE_TIME_MS):

            current_left_position = self.left_rotation_sensor.position(TURNS)
            current_right_position = self.right_rotation_sensor.position(TURNS)

            left_dy = (current_left_position - self.last_left_drivetrain_position_for_speed)
            right_dy = (current_right_position - self.last_right_drivetrain_position_for_speed)

            left_output = left_dy / dx
            right_output = right_dy / dx

            self.previous_left_speeds.append(left_output)
            self.previous_right_speeds.append(right_output)
            self.previous_left_speeds = self.previous_left_speeds[-self.SPEED_SMOOTHING_WINDOW:]
            self.previous_right_speeds = self.previous_right_speeds[-self.SPEED_SMOOTHING_WINDOW:]
            self.last_left_drivetrain_position_for_speed = current_left_position
            self.last_right_drivetrain_position_for_speed = current_right_position
            self.previous_speed_sample_time = current_time

        left_average_speed = sum(self.previous_left_speeds) / len(self.previous_left_speeds)
        right_average_speed = sum(self.previous_right_speeds) / len(self.previous_right_speeds)

        return left_average_speed, right_average_speed

    def get_left_drivetrain_position(self):
        return self.left_rotation_sensor.position(TURNS)

    def get_right_drivetrain_position(self):
        return self.left_rotation_sensor.position(TURNS)

    def get_drivetrain_position(self):
        return MathUtil.average(self.get_left_drivetrain_position(), self.get_right_drivetrain_position())

    def get_drivetrain_speed(self):
        return MathUtil.average_iterable(self.get_drivetrain_speeds())

    def set_speed_rotations_per_second(self, left_speed_rad_per_sec, right_speed_rad_per_sec):
        self.left_drivetrain_PID.setpoint = left_speed_rad_per_sec
        self.right_drivetrain_PID.setpoint = right_speed_rad_per_sec

    def set_speed_percent(self, left_speed_percent, right_speed_percent):
        left_speed_percent /= 100
        right_speed_percent /= 100
        self.set_speed_rotations_per_second(left_speed_percent * self.max_achievable_speed_in_rotations_per_second,
                                            right_speed_percent * self.max_achievable_speed_in_rotations_per_second)

    def update_motor_voltages(self):
        current_left_speed, current_right_speed = self.get_drivetrain_speeds()
        left_controller_output = self.left_drivetrain_PID.update(current_left_speed)
        right_controller_output = self.right_drivetrain_PID.update(current_right_speed)

        self.set_voltage(left_controller_output, right_controller_output)

    def update_odometry(self):
        left_rotation = self.get_left_drivetrain_position()
        right_rotation = self.get_right_drivetrain_position()

        left_delta_rotation = left_rotation - self.last_left_drivetrain_position_for_odometry
        right_delta_rotation = right_rotation - self.last_right_drivetrain_position_for_odometry

        self.last_left_drivetrain_position_for_odometry = left_rotation
        self.last_right_drivetrain_position_for_odometry = right_rotation

        left_distance = Units.radians_to_rotations(left_delta_rotation) * self.wheel_circumference_in_inches * self.motor_to_wheel_gear_ratio
        right_distance = Units.radians_to_rotations(right_delta_rotation) * self.wheel_circumference_in_inches * self.motor_to_wheel_gear_ratio

        average_distance = (left_distance + right_distance) / 2

        self.current_rotation = Rotation2d.from_degrees(self.inertial.rotation(DEGREES))

        self.current_position += Translation2d(Distance.from_inches(average_distance * self.current_rotation.cos()),
                                               Distance.from_inches(average_distance * self.current_rotation.sin()))

    def move_forward_trapezoidal(self, distance):

        # Calculate target position
        target_position = distance

        initial_state = State(self.get_drivetrain_position(), self.get_drivetrain_speed())
        goal_state = State(target_position, 0)

        # Get current time
        start_time = time.time()

        self.trapezoidal_profile.calculate(0, initial_state, goal_state)

        total_time = self.trapezoidal_profile.total_time()

        while time.time() - start_time < total_time + 1:
            target_current_state = self.trapezoidal_profile.calculate(time.time() - start_time, initial_state, goal_state)
            print("TIME: " + str(time.time() - start_time))
            print("TARGET: " + str(target_current_state))

            print("ACTUAL" + str(State(self.get_drivetrain_position(), self.get_drivetrain_speed())))
            print("ACTUAL" + str(self.current_position.x_component.to_inches()))

            self.position_PID.setpoint = target_current_state.position

            output_speed = self.position_PID.update(self.current_position.x_component.to_inches())

            self.set_speed_rotations_per_second(output_speed, output_speed)
            self.update_motor_voltages()
            self.update_odometry()
            # Delay to control loop frequency
            time.sleep(0.01)  # Adjust as necessary

    def turn_to_gyro(self, angle, speed=100):
        self.rotation_PID.setpoint = Rotation2d.from_degrees(angle).to_revolutions()
        self.rotation_PID.reset()
        self.rotation_PID.update(self.current_rotation.to_revolutions())
        while not self.rotation_PID.at_setpoint(threshold=Rotation2d.from_degrees(2).to_revolutions()):
            output = self.rotation_PID.update(self.current_rotation.to_revolutions())
            self.set_speed_percent(output * speed, -output * speed)
            self.update_motor_voltages()
            self.update_odometry()

    def turn_norm_gyro(self, angle, speed=100):
        angle = (Rotation2d.from_degrees(angle) - self.current_rotation.to_revolutions()).normalize()
        self.turn_to_gyro(angle.to_degrees())

    def turn_by_angle(self, angle_degrees):
        target_rotation = self.current_rotation + Rotation2d.from_degrees(angle_degrees)

        self.rotation_PID.setpoint = target_rotation.to_radians()
        self.rotation_PID.update(self.current_rotation.to_radians())
        time.sleep(0.1)  # Adjust as necessary

        while True:
            turning_output = self.rotation_PID.update(self.current_rotation.to_radians())
            if abs(turning_output) < 0.01:
                break
            if turning_output < 0:
                turning_output = MathUtil.clamp(turning_output, None, -3)
            else:
                turning_output = MathUtil.clamp(turning_output, 3, None)

            self.set_speed_percent(-turning_output, turning_output)
            self.update_motor_voltages()
            self.update_odometry()
            time.sleep(0.01)  # Adjust as necessary

    def turn_by_angle_bang_bang(self, angle_degrees):
        target_rotation = self.current_rotation + Rotation2d.from_degrees(angle_degrees)

        turning_output = (self.current_rotation - target_rotation).to_radians()

        last_direction = CLOCKWISE if turning_output < 0 else COUNTERCLOCKWISE

        bangs = 0
        output_magnitude = 50

        while bangs < 3:
            turning_output = (self.current_rotation - target_rotation).to_radians()
            if turning_output < 0:
                if last_direction != CLOCKWISE:
                    last_direction = CLOCKWISE
                    bangs += 1
                    output_magnitude /= 2
                turning_output = output_magnitude
            else:
                if last_direction != COUNTERCLOCKWISE:
                    last_direction = COUNTERCLOCKWISE
                    bangs += 1
                    output_magnitude /= 2
                turning_output = -output_magnitude

            self.set_speed_percent(-turning_output, turning_output)
            self.update_motor_voltages()
            self.update_odometry()

        self.set_speed_percent(0, 0)
        self.update_motor_voltages()

    def turn_by_angle_sqrt(self, angle_degrees):
        target_rotation = self.current_rotation + Rotation2d.from_degrees(angle_degrees)

        def sqrt_function(x):
            return MathUtil.sign(x) * math.sqrt(abs(x) / abs(Units.degrees_to_radians(angle_degrees)))

        turning_output = (self.current_rotation - target_rotation).to_radians()

        output_magnitude = 80

        error_last_5_ticks = [sys.maxsize] * 5

        while sum([abs(error) for error in error_last_5_ticks]) > Units.degrees_to_radians(5):
            turning_output = (self.current_rotation - target_rotation).to_radians()
            error_last_5_ticks.append(turning_output)
            while len(error_last_5_ticks) > 5:
                error_last_5_ticks.pop(0)

            turning_output = MathUtil.clamp(sqrt_function(turning_output) * output_magnitude, -50, 50)

            self.set_speed_percent(turning_output, -turning_output)
            self.update_motor_voltages()
            self.update_odometry()
            time.sleep(0.01)  # Adjust as necessary

        self.set_speed_percent(0, 0)
        self.update_motor_voltages()
