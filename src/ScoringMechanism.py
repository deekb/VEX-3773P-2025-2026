import Constants
from vex import Motor, GearSetting, FORWARD, PERCENT


class ScoringMechanism:
    def __init__(self):
        self.eleven_watt_motor = Motor(Constants.SmartPorts.SCORING_ELEVEN_WATT_MOTOR, GearSetting.RATIO_18_1, False)
        self.five_point_five_watt_motor = Motor(Constants.SmartPorts.SCORING_FIVE_POINT_FIVE_WATT_MOTOR, GearSetting.RATIO_18_1, True)
        self.eleven_watt_motor.spin(FORWARD)
        self.five_point_five_watt_motor.spin(FORWARD)
        self.eleven_watt_motor.set_velocity(0)
        self.five_point_five_watt_motor.set_velocity(0)

    def spin_motor_at_speed(self, speed):
        self.eleven_watt_motor.spin(FORWARD)
        self.eleven_watt_motor.set_velocity(speed, PERCENT)
        self.five_point_five_watt_motor.set_velocity(speed, PERCENT)

    def stop_motor(self):
        self.eleven_watt_motor.spin(FORWARD)
        self.eleven_watt_motor.set_velocity(0, PERCENT)
        self.five_point_five_watt_motor.set_velocity(0, PERCENT)
