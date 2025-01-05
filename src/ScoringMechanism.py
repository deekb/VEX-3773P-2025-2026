from VEXLib.Algorithms.PID import PIDController
from VEXLib.Math import MathUtil

import Constants
from vex import Motor, GearSetting, PERCENT, Thread, VOLT, FORWARD


class ScoringMechanism:
    def __init__(self):
        self.eleven_watt_motor = Motor(Constants.SmartPorts.SCORING_ELEVEN_WATT_MOTOR, GearSetting.RATIO_18_1, False)
        self.five_point_five_watt_motor = Motor(Constants.SmartPorts.SCORING_FIVE_POINT_FIVE_WATT_MOTOR,
                                                GearSetting.RATIO_18_1, True)

    def spin_motor_at_speed(self, speed):
        self.five_point_five_watt_motor.spin(FORWARD, speed * (12 / 100), VOLT)
        self.eleven_watt_motor.spin(FORWARD, speed * (12 / 100), VOLT)

    def stop_motor(self):
        self.five_point_five_watt_motor.spin(FORWARD, 0, VOLT)
        self.eleven_watt_motor.spin(FORWARD, 0, VOLT)

    def intake(self):
        self.spin_motor_at_speed(100)

    def outtake(self):
        self.spin_motor_at_speed(-100)
