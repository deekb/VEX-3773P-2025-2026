from VEXLib.Motor import Motor
from VEXLib.Util import time
from vex import DigitalOut, TorqueUnits, PERCENT, Color, Optical, Thread, FORWARD, HOLD, COAST


class IntakeV2:
    def __init__(self, upper_intake_motor: Motor, floating_intake_motor: Motor, hood_motor: Motor, piston: DigitalOut, color_sensor: Optical):
        self.PASSIVE_SPEED = 0.2

        self.upper_intake_motor = upper_intake_motor
        self.floating_intake_motor = floating_intake_motor
        self.hood_motor = hood_motor
        self.piston = piston
        self.optical = color_sensor
        self.optical.set_light_power(100)
        self.last_not_stalled_timestamp = time.time()
        self.stop_hood()

    def run_upper_intake(self, speed):
        """Run the upper intake motor at a specified speed."""
        self.upper_intake_motor.set(speed)

    def stop_upper_intake(self):
        """Stop the upper intake motor"""
        self.upper_intake_motor.set(0)

    def run_floating_intake(self, speed):
        """Run the upper intake motor at a specified speed."""
        self.floating_intake_motor.set(speed)

    def stop_floating_intake(self):
        """Stop the upper intake motor"""
        self.floating_intake_motor.set(0)

    def run_hood(self, speed):
        """Run the hood motor at a specified speed."""
        if speed == 0:
            # self.hood_motor.set(-self.PASSIVE_SPEED)
            self.hood_motor.set_stopping(HOLD)
            self.hood_motor.set_velocity(0)
            self.hood_motor.stop()
        else:
            self.hood_motor.set_stopping(COAST)
            self.hood_motor.set(speed)

    def stop_hood(self):
        """Stop the hood motor."""
        self.run_hood(0)

    def run_intake(self, speed):
        """Run the full intake motor at a specified speed."""
        self.run_floating_intake(speed)
        self.run_upper_intake(speed)
        self.run_hood(speed)

    def stop_intake(self):
        """Stop the full intake"""
        self.run_floating_intake(0)
        self.run_upper_intake(0)
        self.run_hood(0)

    def raise_intake(self):
        """Raise the intake piston."""
        self.piston.set(True)

    def lower_intake(self):
        """Lower the intake piston."""
        self.piston.set(False)

    def toggle_intake_piston(self):
        """Toggle the intake piston."""
        self.piston.set(not self.piston.value())

    def get_color(self):
        """Get the current color."""
        hue = self.optical.hue()
        if not self.optical.is_near_object():
            return None
        if 0 < hue < 20:
            return Color.RED
        if 180 < hue < 240:
            return Color.BLUE
        return None
        # Blue is hue 180 to 220
        # Red is hue 0 to 20

    def intake_until_color(self, color: Color, speed = 1, timeout = 3):
        self.run_intake(speed)
        start_time = time.time()
        while not self.get_color() == color and time.time() - start_time < timeout:
            time.sleep_ms(2)
        if time.time() - start_time > timeout:
            return
        self.stop_intake()
        self.run_hood(-1)
        time.sleep_ms(100)
        self.stop_intake()

    def intake_until_color_nonblocking(self, color: Color, speed = 1, timeout = 3):
        Thread(self.intake_until_color, (color, speed, timeout))

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

    def pickup(self, speed=1):
        self.run_floating_intake(speed)
        self.run_upper_intake(speed)
