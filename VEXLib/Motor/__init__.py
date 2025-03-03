import math

import vex
from vex import Motor as vexMotor, GearSetting, DEGREES, RPM, VOLT, Thread
from ..Algorithms.PID import PIDController
from ..Util import time as time
from .Constants import *


class Motor(vex.Motor):
    def __init__(self, port, gear_ratio, inverted):
        super().__init__(port, gear_ratio, inverted)

    def set(self, power):
        self.spin(FORWARD, power * 12, VOLT)

# class Motor:
#     def __init__(self, port, gear_ratio=18, direction=FORWARD, run_mode=NONE):
#         # We are running all motors at 18:1 gear ratio and compensating for it in the get_position and get_velocity methods
#         # This is so that we can define custom gear ratios that include gears external to the motor
#         self.port = port
#         self._motor = vexMotor(port, GearSetting.RATIO_18_1, FORWARD)
#         self.gear_ratio = gear_ratio
#         self.direction = direction
#         self.run_type = run_mode
#         self._encoder_offset = 0
#         self._velocity_setpoint = 0
#         self._position_setpoint = 0
#         self.position_pid = PIDController(0, 0, 0, 0.05)
#         self.velocity_pid = PIDController(0, 0, 0, 0.05)
#         Thread(self.update_loop)
#
#     def set_direction(self, direction):
#         self.direction = direction
#
#     def get_direction(self):
#         return self.direction
#
#     def set_target_velocity(self, velocity):
#         if abs(velocity) > 1:
#             raise ValueError("Velocity must be between -1 and 1")
#         self._velocity_setpoint = velocity
#
#     def set_target_position(self, position):
#         self._position_setpoint = position
#
#     def update_loop(self):
#         while True:
#             time.sleep(0.05)
#             self.update_pid()
#
#     def update_pid(self):
#         if self.run_type == PID_VELOCITY_CONTROL:
#             # TODO: Get this working
#             speed = self.velocity_pid.update(self.get_velocity_rotations_per_minute())
#         elif self.run_type == PID_POSITION_CONTROL:
#             speed = self.position_pid.update(self.get_position_degrees())
#
#         else:
#             speed = self._velocity_setpoint
#
#         self._motor.set_velocity(speed * (-100 if self.direction == REVERSE else 100))
#
#     def set_voltage(self, voltage):
#         if abs(voltage) > 12:
#             raise ValueError("Voltage must be between -12 and 12")
#         self._motor.spin(FORWARD, voltage * (-1 if self.direction == REVERSE else 1), VOLT)
#
#     def reset_encoder(self):
#         self._encoder_offset = self.get_position_degrees()
#
#     def set_encoder_position_degrees(self, position):
#         self._encoder_offset = self.get_position_degrees() + position
#
#     def get_position_degrees(self):
#         return self._motor.position(DEGREES) - self._encoder_offset
#
#     def get_position_turns(self):
#         return self.get_position_degrees() / 360
#
#     def get_position_radians(self):
#         return math.radians(self.get_position_degrees())
#
#     def get_velocity_rotations_per_minute(self):
#         return (self._motor.velocity(RPM) / (1 / 18)) / self.gear_ratio
#
#     def get_velocity_rotations_per_second(self):
#         return self.get_velocity_rotations_per_minute() / 60
#
#     def get_velocity_degrees_per_second(self):
#         return self.get_velocity_rotations_per_second() * 360
#
#     def get_velocity_radians_per_second(self):
#         return math.radians(self.get_velocity_degrees_per_second())

# class FixedMotor(Motor):
#     def __init__(self, port, gear_ration, reversed_, speed_smoothing_window=5):
#         super().__init__(port, gear_ration, reversed_)
#         self.last_position = 0
#         self.speed_smoothing_window = speed_smoothing_window
#
#         self.thread = Thread(self._mainloop)
#
#     def mainloop(self):
#         while True:
#             self._tick()
#
#     def _tick(self):
#         x = x
#
#
#     def update_drivetrain_velocities(self):
#         current_time = ContinuousTimer.time()
#         dx = (current_time - self.previous_speed_sample_time)
#         if dx >= Units.milliseconds_to_seconds(self.SPEED_SAMPLE_TIME_MS):
#             current_left_position = self.left_rotation_sensor.position(TURNS)
#             current_right_position = self.right_rotation_sensor.position(TURNS)
#
#             left_dy = (current_left_position - self.last_left_drivetrain_position)
#             right_dy = (current_right_position - self.last_right_drivetrain_position)
#
#             left_output = left_dy / dx
#             right_output = right_dy / dx
#
#             self.previous_left_speeds.append(left_output)
#             self.previous_right_speeds.append(right_output)
#             self.previous_left_speeds = self.previous_left_speeds[-self.SPEED_SMOOTHING_WINDOW:]
#             self.previous_right_speeds = self.previous_right_speeds[-self.SPEED_SMOOTHING_WINDOW:]
#             self.last_left_drivetrain_position = current_left_position
#             self.last_right_drivetrain_position = current_right_position
#             self.previous_speed_sample_time = current_time
#
#         left_average_speed = sum(self.previous_left_speeds) / len(self.previous_left_speeds)
#         right_average_speed = sum(self.previous_right_speeds) / len(self.previous_right_speeds)
#
#         return left_average_speed, right_average_speed
#
#
#     def velocity(self, *args):
#         return 0
#
#     def
