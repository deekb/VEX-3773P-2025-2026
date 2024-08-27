from math import sin

import Constants
from VEXLib.Util import time
from vex import Motor, GearSetting, DigitalOut, Limit, FORWARD


class ScoringMechanism:
    def __init__(self, wiggle_frequency, wiggle_amplitude):
        self.motor = Motor(Constants.SmartPorts.SCORING_MOTOR, GearSetting.RATIO_18_1, False)
        self.pto_piston = DigitalOut(Constants.ThreeWirePorts.PTO_PISTON)
        self.limit_switch = Limit(Constants.ThreeWirePorts.LIMIT_SWITCH)
        self.motor.spin(FORWARD)
        self.motor.set_velocity(0)
        self.WIGGLE_FREQUENCY = wiggle_frequency
        self.WIGGLE_AMPLITUDE = wiggle_amplitude

    def extend_piston(self):
        self.pto_piston.set(True)

    def retract_piston(self):
        self.pto_piston.set(False)

    def spin_motor_at_speed(self, speed):
        self.motor.set_velocity(speed)

    def stop_motor(self):
        self.motor.set_velocity(0)

    def score_on_mobile_goal(self):
        self.extend_piston()
        self.spin_motor_at_speed(-50)

    def raise_intake(self):
        self.retract_piston()
        self.spin_motor_at_speed(50)

    def is_piston_extended(self):
        return not self.limit_switch.pressing()

    def _calculate_wiggle(self, time):
        return self.WIGGLE_AMPLITUDE * sin(self.WIGGLE_FREQUENCY * time)

    def wiggle(self):
        self.spin_motor_at_speed(self._calculate_wiggle(time.time()))
