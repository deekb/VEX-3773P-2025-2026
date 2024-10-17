import Constants
from vex import Motor, GearSetting, FORWARD, PERCENT


class ScoringMechanism:
    def __init__(self):
        self.motor = Motor(Constants.SmartPorts.SCORING_MOTOR, GearSetting.RATIO_18_1, False)
        self.motor.spin(FORWARD)
        self.motor.set_velocity(0)

    def spin_motor_at_speed(self, speed):
        self.motor.set_velocity(speed, PERCENT)

    def stop_motor(self):
        self.motor.set_velocity(0, PERCENT)
