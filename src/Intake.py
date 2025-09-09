from VEXLib.Motor import Motor

class Intake:
    def __init__(self, lower_motor: Motor, upper_motor: Motor, bucket_motor: Motor):
        self.lower_motor = lower_motor
        self.upper_motor = upper_motor
        self.bucket_motor = bucket_motor
        self.bucket_locked = False  # Initialize bucket lock state

    def run_lower(self, speed):
        """Run the lower intake motor at a specified speed."""
        self.lower_motor.set(speed)

    def stop_lower(self):
        """Stop the lower intake motor."""
        self.lower_motor.set(0)

    def run_upper(self, speed):
        """Run the upper intake motor at a specified speed."""
        self.upper_motor.set(speed)

    def stop_upper(self):
        """Stop the upper intake motor."""
        self.upper_motor.set(0)

    def run_bucket(self, speed):
        """Run the bucket motor at a specified speed."""
        if not self.bucket_locked:
            self.bucket_motor.set(speed)

    def stop_bucket(self):
        """Stop the bucket motor."""
        self.bucket_motor.set(0)

    def toggle_bucket_lock(self):
        """Toggle the bucket lock state."""
        self.bucket_locked = not self.bucket_locked
        if self.bucket_locked:
            self.stop_bucket()

    def set_bucket_lock(self, locked: bool):
        """Set the bucket to a locked state."""
        self.bucket_locked = locked
        if locked:
            self.stop_bucket()