from VEXLib.Motor import Motor
from VEXLib.Util import time
from vex import DigitalOut, TorqueUnits, PERCENT


class Intake:
    def __init__(self, upper_intake_motor: Motor, floating_intake_motor: Motor, hood_motor: Motor, piston: DigitalOut):
        self.upper_intake_motor = upper_intake_motor
        self.floating_intake_motor = floating_intake_motor
        self.hood_motor = hood_motor
        self.piston = piston
        self.last_not_stalled_timestamp = time.time()

    def run_floating_intake(self, speed):
        """Run the floating intake motor at a specified speed."""
        self.floating_intake_motor.set(speed)

    def stop_floating_intake(self):
        """Stop the floating intake motor"""
        self.floating_intake_motor.set(0)

    def run_upper_intake(self, speed):
        """Run the upper intake motor at a specified speed."""
        self.upper_intake_motor.set(speed)

    def stop_upper_intake(self):
        """Stop the upper intake motor"""
        self.upper_intake_motor.set(0)

    def run_hood(self, speed):
        """Run the hood motor at a specified speed."""
        self.hood_motor.set(speed)

    def stop_hood(self):
        """Stop the hood motor."""
        self.hood_motor.set(0)

    def run_intake(self, speed):
        """Run the full intake motor at a specified speed."""
        self.run_upper_intake(speed)
        self.run_floating_intake(speed)
        self.run_hood(speed)

    def stop_intake(self):
        """Stop the full intake"""
        self.run_upper_intake(0)
        self.run_floating_intake(0)
        self.run_hood(0)

    def raise_intake(self):
        """Raise the intake piston."""
        self.piston.set(False)

    def lower_intake(self):
        """Lower the intake piston."""
        self.piston.set(True)

    def toggle_intake_piston(self):
        """Toggle the intake piston."""
        self.piston.set(not self.piston.value())

    def flaps_are_stalled(self):
         # Stall if torque is high and velocity is low
         torque_threshold = 1  # Adjust as needed
         velocity_threshold = 10  # Adjust as needed

         is_stalled = (
             self.upper_intake_motor.get() != 0 and
             self.upper_intake_motor.torque(TorqueUnits.NM) > torque_threshold and
             abs(self.upper_intake_motor.velocity(PERCENT)) < velocity_threshold
         )

         current_time = time.time()
         if not is_stalled:
            self.last_not_stalled_timestamp = current_time

         # Only report stall if the condition has persisted for at least 0.1s
         stalled_duration = current_time - self.last_not_stalled_timestamp
         return is_stalled and stalled_duration > 0.1
