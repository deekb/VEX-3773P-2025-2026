from vex import VOLT, FORWARD


class ScoringMechanism:
    def __init__(self, motors):
        self.motors = motors

    def spin_motor_at_speed(self, speed):
        for motor in self.motors:
            motor.spin(FORWARD, speed * (12 / 100), VOLT)

    def stop_motor(self):
        for motor in self.motors:
            motor.spin(FORWARD, 0, VOLT)

    def intake(self):
        self.spin_motor_at_speed(100)

    def outtake(self):
        self.spin_motor_at_speed(-100)
