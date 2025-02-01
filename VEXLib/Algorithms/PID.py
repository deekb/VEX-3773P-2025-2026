from vex import Thread, wait, PERCENT, RPM, SECONDS
from ..Math import MathUtil
from VEXLib.Units import Units
from ..Util import time as time


class PIDMotorController:
    """
    Wrap a motor definition in this class to use a custom PID to control its movements ie: my_tunable_PID_motor = MotorPID(Motor(...), PID_controller)
    **Waring, this class disables all motor functionality except the following functions:[set_target_velocity_<unit>, stop, spin, get_velocity_<unit>]**
    """

    def __init__(self, motor, pid_controller):
        """
        Creates an instance of the MotorPID

        Args:
            motor: The motor to apply the PID to
            pid_controller: The PID controller for
        """
        self.motor = motor
        self.PID_controller = pid_controller
        self.pid_thread = Thread(self._loop)

    def update(self) -> None:
        """
        Update the PID state with the most recent motor and target velocities and send the normalized value to the motor
        """

        self.motor.set_velocity(self.PID_controller.update(self.get_velocity_rads_per_second()), PERCENT)

    def _loop(self) -> None:
        """
        Used to run the PID in a new thread: updates the values the PID uses and handles
          applying the PID output to the motor
        """

        while True:
            self.update()
            wait(self.PID_controller.t, SECONDS)

    def set_target_velocity_rad_per_second(self, velocity: float) -> None:
        """
        Set the motor's target velocity using the PID, make sure you run PID_loop in a new thread or this
        will have no effect
        :param velocity: The new target velocity of the motor
        :type velocity: float
        """

        self.PID_controller.setpoint = velocity

    def stop(self):
        self.set_target_velocity_rad_per_second(0)

    def get_velocity_rotations_per_minute(self):
        return self.motor.velocity(RPM)

    def get_velocity_rads_per_second(self):
        return Units.rotations_per_minute_to_radians_per_second(self.get_velocity_rotations_per_minute())

    def get_velocity_rotations_per_second(self):
        return Units.rotations_per_minute_to_rotations_per_second(self.get_velocity_rotations_per_minute())


class PIDController:
    def __init__(self, kp: float = 1.0,
                 ki: float = 0.0,
                 kd: float = 0.0,
                 t: float = 0.05,
                 integral_limit: float = 1.0):
        """
        Initializes a PIDController instance.

        Args:
            kp: Kp value for the PID.
            ki: Ki value for the PID.
            kd: Kd value for the PID.
            t: Minimum time between update calls. All calls made before this amount of time has passed since the last calculation will be ignored.
            integral_limit: The maximum absolute value for the integral term to prevent windup.
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.time_step = t
        self._previous_time = time.time()
        self._current_value = 0.0
        self.setpoint = 0.0
        self._error_integral = 0.0
        self._integral_limit = integral_limit
        self._previous_error = 0.0
        self._control_output = 0.0

    def update(self, current_value: float) -> float:
        """
        Update the PID state with the most recent current value and calculate the control output.

        Args:
            current_value: The current measurement or feedback value

        Returns:
            The calculated control output.
        """
        current_time = time.time()
        delta_time = current_time - self._previous_time

        if delta_time < self.time_step:
            # If the elapsed time since the last calculation is less than the time step, then
            # return the last output without recalculating
            return self._control_output

        self._previous_time = current_time
        self._current_value = current_value

        # Calculate the error and adjust for continuous input if enabled
        current_error = self.setpoint - self._current_value
        # current_error = self._calculate_continuous_error(current_error)

        self._error_integral += current_error * delta_time
        if self.ki != 0:
            self._error_integral = MathUtil.clamp(self._error_integral, -self._integral_limit, self._integral_limit)
        if self.kd != 0:
            error_derivative = (current_error - self._previous_error) / delta_time
        else:
            error_derivative = 0.0

        self._control_output = (
                self.kp * current_error + self.ki * self._error_integral + self.kd * error_derivative
        )
        self._previous_error = current_error
        return self._control_output

    def at_setpoint(self, threshold=0.05):
        return abs(self._previous_error) <= threshold

    def reset(self):
        print("RESET PID")
        self._current_value = 0
        self._previous_error = 0
        self._error_integral = 0
        self._control_output = 0
