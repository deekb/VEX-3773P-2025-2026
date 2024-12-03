from VEXLib.Math import clamp, MathUtil

import Constants
from VEXLib.Util import time
from vex import Motor, GearSetting, FORWARD, PERCENT, DEGREES, HOLD, Thread, BRAKE, REVERSE, VOLT, DigitalIn, \
    wait, MSEC, Limit


class WallStakeMechanism:
    """
    A class representing the wall stake mechanism used for scoring in a VEX Robotics system.
    The mechanism uses a motor to control movement and provides functionality for docking, scoring,
    and managing motor velocity and position.
    """

    def __init__(self):
        """
        Initializes the WallStakeMechanism object.

        The motor is set up with a gear ratio of 36:1, and the initial position and velocity are configured.
        A separate thread is used to continuously monitor the state of the mechanism.

        Attributes:
            motor (vex.Motor): The motor controlling the wall stake mechanism.
            docking (bool): Whether the mechanism is currently docking.
            thread (vex.Thread): A thread that runs the `tick` method to handle real-time operations.
        """
        self.manual_control = True

        self.limit_switch = Limit(Constants.ThreeWirePorts.WALL_STAKE_CALIBRATION_LIMIT_SWITCH)
        self.motor = Motor(Constants.SmartPorts.WALL_STAKE_MOTOR, GearSetting.RATIO_36_1, True)
        self.motor.spin(FORWARD)
        self.motor.set_velocity(0)
        self.target_velocity = 0

        self.DOCKING_POSITION = 10
        self.SCORING_POSITION = 645

    def calibrate(self):
        while not self.limit_switch.pressing():
            self.motor.spin(FORWARD, -5, VOLT)
            wait(10, MSEC)

        while self.limit_switch.pressing():
            self.motor.spin(FORWARD, 5, VOLT)
            wait(10, MSEC)

        self.motor.set_position(0, DEGREES)
        self.motor.set_velocity(0, PERCENT)
        self.motor.spin(FORWARD)

    def move_out(self):
        """
        Starts the process of docking the wall stake mechanism.

        The motor is set to move backward at a defined speed to dock the mechanism.
        """
        self.manual_control = True
        self.target_velocity = -Constants.ScoringMechanismProperties.SCORING_SPEED_PERCENT

    def move_in(self):
        """
        Starts the process of moving the wall stake mechanism to score a ring.

        The motor is set to move forward at a defined speed to extend the mechanism.
        """
        self.manual_control = True
        self.target_velocity = Constants.ScoringMechanismProperties.SCORING_SPEED_PERCENT

    def dock(self):
        self.manual_control = False
        self.motor.set_velocity(75, PERCENT)
        self.motor.spin_to_position(self.DOCKING_POSITION, DEGREES, wait=False)

    def score(self):
        self.manual_control = False
        self.motor.set_velocity(75, PERCENT)
        self.motor.spin_to_position(self.SCORING_POSITION, DEGREES, wait=False)

    def stop(self):
        """
        Stops the movement of the wall stake mechanism.

        The motor is paused and placed into PID hold mode to maintain its position.
        """
        self.target_velocity = 0

    def tick(self):
        """
        Monitors the state of the wall stake mechanism in real-time.

        This method continuously checks the motor's position to determine if docking is complete
        or if the mechanism has reached the maximum position. If conditions are met, the motor's velocity is set to 0
        and the motor is set to COAST mode to prevent power consumption and overheating when idle. The method is run in
        a thread that belongs to the class instance.

        The method sleeps for 50 milliseconds between checks.
        """
        if self.limit_switch.pressing():
            self.motor.set_stopping(BRAKE)
        else:
            self.motor.set_stopping(HOLD)

        if self.manual_control:
            if self.limit_switch.pressing():
                self.target_velocity = MathUtil.clamp(self.target_velocity, 0, None)

            if self.motor.position(DEGREES) > 645:
                self.target_velocity = clamp(self.target_velocity, None, 0)

            self.motor.spin(FORWARD)
            self.motor.set_velocity(self.target_velocity, PERCENT)
