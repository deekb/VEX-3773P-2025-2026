import Constants
from VEXLib.Util import time
from vex import Motor, GearSetting, FORWARD, PERCENT, DEGREES, HOLD, Thread, COAST, BRAKE, REVERSE, VOLT


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
        self.motor = Motor(Constants.SmartPorts.WALL_STAKE_MOTOR, GearSetting.RATIO_36_1, True)
        self.motor.set_stopping(HOLD)
        self.motor.spin(FORWARD)
        self.motor.set_velocity(0)
        self.motor.set_position(Constants.ScoringMechanismProperties.STARTUP_POSITION, DEGREES)
        self.docking = False
        # self.thread = Thread(self.tick)

    # def calibrate(self):
    #     self.motor.spin(REVERSE, 6, VOLT)
    #     wait(200, MSEC)
    #     while motor.velocity(PERCENT) > 2:
    #         wait(10, MSEC)
    #     self.motor.set_velocity(0, PERCENT)
    #     self.motor.spin(FORWARD)


    def dock(self):
        """
        Initiates the docking process.

        The motor starts moving the mechanism to dock by setting the motor's velocity to a negative number.
        """
        self.docking = True
        self.motor.set_velocity(-Constants.ScoringMechanismProperties.SCORING_SPEED_PERCENT, PERCENT)

    def start_docking(self):
        """
        Starts the process of docking the wall stake mechanism.

        The motor is set to move backward at a defined speed to dock the mechanism.
        """
        self.docking = False
        # self.motor.spin(FORWARD)
        self.motor.set_velocity(-Constants.ScoringMechanismProperties.SCORING_SPEED_PERCENT, PERCENT)

    def start_scoring(self):
        """
        Starts the process of moving the wall stake mechanism to score a ring.

        The motor is set to move forward at a defined speed to extend the mechanism.
        """
        self.docking = False
        # self.motor.spin(FORWARD)
        self.motor.set_velocity(Constants.ScoringMechanismProperties.SCORING_SPEED_PERCENT, PERCENT)

    def stop(self):
        """
        Stops the movement of the wall stake mechanism.

        The motor is paused and placed into PID hold mode to maintain its position.
        """
        self.motor.set_velocity(0, PERCENT)
        self.motor.set_stopping(HOLD)

    def tick(self):
        """
        Monitors the state of the wall stake mechanism in real-time.

        This method continuously checks the motor's position to determine if docking is complete
        or if the mechanism has reached the maximum position. If conditions are met, the motor's velocity is set to 0
        and the motor is set to COAST mode to prevent power consumption and overheating when idle. The method is run in
        a thread that belongs to the class instance.

        The method sleeps for 50 milliseconds between checks.
        """
        while True:

            # if self.docking:
            #     if abs(self.motor.position(DEGREES)) < 5:
            #         self.docking = False
            #         self.motor.set_velocity(0, PERCENT)
            #         self.motor.set_stopping(COAST)
            # if self.motor.position(DEGREES) > Constants.ScoringMechanismProperties.MAX_POSITION:
            #     self.motor.set_velocity(0, PERCENT)

            if abs(self.motor.position(DEGREES)) < 500:
                self.motor.set_stopping(BRAKE)
            else:
                self.motor.set_stopping(HOLD)
            time.sleep(0.05)
