from VEXLib.Math import MathUtil
from VEXLib.Motor import Motor
from VEXLib.Util import time
from Constants import IntakeConstants
from vex import DigitalOut, TorqueUnits, PERCENT, Color, Optical, Thread, FORWARD, HOLD, COAST, DEGREES


class Intake:
    def __init__(self, lever_motor: Motor, floating_intake_motor: Motor, flap_piston: DigitalOut, raise_piston: DigitalOut):
        self.lever_motor = lever_motor
        self.floating_intake_motor = floating_intake_motor
        self.flap_piston = flap_piston
        self.raise_piston = raise_piston
        self.lever_target = 0
        self.lever_speed = 0
        self.time_updated_setpoint = 0
        self.lever_step_amount = 20
        self.lever_motor.spin(FORWARD)
        self.set_lever_velocity(0)

    def set_lever_velocity(self, velocity):
        self.lever_motor.spin(FORWARD)
        self.lever_motor.set_velocity(velocity)

    def move_lever_to_position(self, position_deg):
        self.lever_motor.set_velocity(IntakeConstants.RETURN_SPEED, PERCENT)
        self.lever_motor.spin_to_position(position_deg, DEGREES)

    def move_lever_down(self):
        self.set_lever_speed(100)
        self.set_lever_setpoint(0)

    def set_lever_setpoint(self, setpoint):
        self.lever_target = setpoint
        self.time_updated_setpoint = time.time()

    def set_lever_speed(self, speed):
        self.lever_speed = speed

    def run_floating_intake(self, speed = 1):
        """Run the upper intake motor at a specified speed."""
        self.floating_intake_motor.set(speed)

    def stop_floating_intake(self):
        """Stop the upper intake motor"""
        self.floating_intake_motor.set(0)

    def raise_intake(self):
        """Raise the intake piston."""
        self.raise_piston.set(True)

    def lower_intake(self):
        """Lower the intake piston."""
        self.raise_piston.set(False)

    def toggle_intake_piston(self):
        """Toggle the intake piston."""
        self.raise_piston.set(not self.raise_piston.value())

    def extend_flap(self):
        """Raise the intake piston."""
        self.flap_piston.set(True)

    def retract_flap(self):
        """Lower the intake piston."""
        self.flap_piston.set(False)

    def toggle_flap_piston(self):
        """Toggle the intake piston."""
        self.raise_piston.set(not self.flap_piston.value())

    def step_up(self):
        self.set_lever_setpoint(self.lever_target + self.lever_step_amount)

    def lever_is_stalled(self):
        # Stall if torque is high and velocity is low
        torque_threshold = 1  # Adjust as needed
        velocity_threshold = 10  # Adjust as needed

        is_stalled = (
             self.lever_motor.get() != 0 and
             self.lever_motor.torque(TorqueUnits.NM) > torque_threshold and
             abs(self.lever_motor.velocity(PERCENT)) < velocity_threshold
         )

        current_time = time.time()
        if not is_stalled:
            self.last_not_stalled_timestamp = current_time

        # Only report stall if the condition has persisted for at least 0.1s
        stalled_duration = current_time - self.last_not_stalled_timestamp
        return is_stalled and stalled_duration > 0.1

    def periodic(self):
        error = self.lever_target - self.lever_motor.position(DEGREES)
        if MathUtil.is_near(self.lever_target, self.lever_motor.position(DEGREES), 3):
            self.set_lever_velocity(0)
        else:
            self.set_lever_velocity(MathUtil.clamp(self.lever_speed * error * 0.1, -self.lever_speed, self.lever_speed))

        # Check if we should return to lowered setpoint
        # If we are

        # time_since_setpoint_changed = time.time() - self.time_updated_setpoint
        #
        # if self.lever_target != 0 and time_since_setpoint_changed > 1:
        #     self.set_lever_setpoint(0)
