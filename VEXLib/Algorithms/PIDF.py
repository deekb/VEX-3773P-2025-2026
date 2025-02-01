from ..Algorithms.PID import PIDController
from VEXLib.Util import time


class PIDFController(PIDController):
    """
    A PID controller with a feedforward term.
    """

    def __init__(
            self,
            kp: float = 1.0,
            ki: float = 0.0,
            kd: float = 0.0,
            kf: float = 0.0,  # New feedforward term
            t: float = 0.05,
            integral_limit: float = 1.0,
    ):
        """
        Initializes a PIDFController instance.

        Args:
            kp: Kp value for the PID.
            ki: Ki value for the PID.
            kd: Kd value for the PID.
            kf: Kf value for the feedforward.
            t: Minimum time between update calls. All calls made before this amount of time has passed since the last calculation will be ignored.
            integral_limit: The maximum absolute value for the integral term to prevent windup.
        """
        # Call the constructor of the base class (PIDController)
        super().__init__(kp, ki, kd, t, integral_limit)
        # Additional initialization for feedforward term
        self.kf = kf

    def update(self, current_value: float) -> float:
        """
        Update the PIDF controller state with the most recent current value and calculate the control output.

        Args:
            current_value: The current measurement or feedback value

        Returns:
            The calculated control output.
        """
        # Call the update method of the base class (PIDController)
        pid_output = super().update(current_value)
        # Calculate the feedforward component
        feedforward_output = self.kf * self.setpoint
        # Combine PID and feedforward outputs
        total_output = pid_output + feedforward_output
        return total_output

#
# class ProfiledPIDFController(PIDFController):
#     def __init__(
#             self,
#             kp: float = 1.0,
#             ki: float = 0.0,
#             kd: float = 0.0,
#             kf: float = 0.0,
#             t: float = 0.05,
#             integral_limit: float = 1.0,
#             max_acceleration: float = 1.0,
#             max_velocity: float = 1.0
#     ):
#         super().__init__(kp, ki, kd, kf, t, integral_limit)
#         self.max_acceleration = max_acceleration
#         self.max_velocity = max_velocity
#         self.current_velocity = 0.0
#         self.target_velocity = 0.0
#         self.last_time = None
#
#     def set_target_velocity(self, target_velocity):
#         self.target_velocity = target_velocity
#
#     def update(self, current_value: float) -> float:
#         current_time = time.time()
#         if self.last_time is None:
#             self.last_time = current_time
#
#         delta_time = current_time - self.last_time
#         self.last_time = current_time
#
#         if delta_time > 0:
#             velocity_error = self.target_velocity - self.current_velocity
#
#             if abs(velocity_error) < self.max_acceleration * delta_time:
#                 # If the velocity error is less than what we can change in this time step, just set it directly
#                 self.current_velocity = self.target_velocity
#             else:
#                 # Calculate the desired acceleration, making sure it's within our limits
#                 desired_acceleration = self.max_acceleration if velocity_error > 0 else -self.max_acceleration
#                 self.current_velocity += desired_acceleration * delta_time
#
#             # Clamp the velocity to the max_velocity
#             self.current_velocity = max(min(self.current_velocity, self.max_velocity), -self.max_velocity)
#
#         return super().update(current_value)
