from Constants import WallStakeMechanismProperties
from VEXLib.Algorithms.GravitationalFeedforward import GravitationalFeedforward
from VEXLib.Algorithms.PID import PIDController
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Util import time
from VEXLib.Util.Logging import Logger
from vex import FORWARD, DEGREES, VOLT, Rotation, Thread, Brain


class WallStakeState:
    DOCKED = 1
    LOADING = 2
    HIGH_SCORING = 3
    LOW_SCORING = 4


wall_stake_mechanism_logger = Logger(
    Brain().sdcard, Brain().screen, "WallStakeMechanism"
)


class WallStakeMechanism:
    """
    A class representing the wall stake mechanism.
    The mechanism uses a motor to control movement and provides a state machine
    for managing the setpoint of the mechanism
    """

    def __init__(self, motor, rotation_sensor: Rotation):
        """
        Initializes the WallStakeMechanism subsystem.

        Attributes:
            motor (Motor): The motor controlling the wall stake mechanism.
            rotation_sensor (Rotation): The rotation sensor used to measure the mechanism's position.
        """
        self.rotation_sensor = rotation_sensor
        self.motor = motor

        self.log = wall_stake_mechanism_logger

        self.PID_GAINS = WallStakeMechanismProperties.PID_GAINS
        self.FEEDFORWARD_GAIN = WallStakeMechanismProperties.FEEDFORWARD_GAIN
        self.DOCKED_POSITION = WallStakeMechanismProperties.DOCKED_POSITION
        self.POSITIONAL_TOLERANCE = WallStakeMechanismProperties.POSITIONAL_TOLERANCE
        self.LOADING_POSITION = WallStakeMechanismProperties.LOADING_POSITION
        self.HIGH_SCORING_POSITION = WallStakeMechanismProperties.HIGH_SCORING_POSITION
        self.LOW_SCORING_POSITION = WallStakeMechanismProperties.LOW_SCORING_POSITION
        self.UPRIGHT_POSITION = WallStakeMechanismProperties.UPRIGHT_POSITION

        self.gravitational_feedforward = GravitationalFeedforward(self.FEEDFORWARD_GAIN)
        self.pid = PIDController(self.PID_GAINS)

        self.state = WallStakeState.DOCKED

        # Call transition_to to ensure we are really in the initial state
        self.transition_to(self.state)
        self.log.info("WallStakeMechanism initialized with state: DOCKED")
        self.log.info("Starting loop thread")
        self.tick_thread = Thread(self.loop)

    def update_motor_voltage(self):
        # self.log.trace("Entering update_motor_voltage")
        current_rotation = Rotation2d.from_degrees(
            self.rotation_sensor.position(DEGREES)
        )
        feedforward_output = self.gravitational_feedforward.update(
            current_rotation.to_degrees()
        )
        pid_output = self.pid.update(current_rotation.normalize().to_revolutions())

        # self.log.debug("Current rotation: {} degrees".format(current_rotation.to_degrees()))
        # self.log.debug("Feedforward output: {}, PID output: {}".format(feedforward_output, pid_output))

        if self.state == WallStakeState.DOCKED and self.at_setpoint():
            self.motor.spin(FORWARD, 0, VOLT)
            # self.log.info("Motor stopped as the mechanism is docked and at setpoint")
            return

        self.motor.spin(FORWARD, feedforward_output - pid_output, VOLT)
        # self.log.debug("Motor voltage set to: {} VOLT".format(feedforward_output - pid_output))

    @wall_stake_mechanism_logger.logged
    def transition_to(self, new_state):
        if new_state == WallStakeState.DOCKED:
            self.log.info("Transitioning to Docked")
            self.pid.setpoint = self.DOCKED_POSITION.to_revolutions()
        elif new_state == WallStakeState.LOADING:
            self.log.info("Transitioning to Loading")
            self.pid.setpoint = self.LOADING_POSITION.to_revolutions()
        elif new_state == WallStakeState.HIGH_SCORING:
            self.log.info("Transitioning to High Scoring")
            self.pid.setpoint = self.HIGH_SCORING_POSITION.to_revolutions()
        elif new_state == WallStakeState.LOW_SCORING:
            self.log.info("Transitioning to Low Scoring")
            self.pid.setpoint = self.LOW_SCORING_POSITION.to_revolutions()

        self.state = new_state
        self.log.debug("New state set: {}".format(new_state))

    def next_state(self):
        self.log.trace("Entering next_state")
        if self.state == 4:
            self.log.warn(
                "Already in the highest state, cannot transition to next state"
            )
            return
        self.transition_to(self.state + 1)
        self.log.info("Transitioned to next state:", self.state)

    def previous_state(self):
        self.log.trace("Entering previous_state")
        if self.state == 1:
            self.log.warn(
                "Already in the lowest state, cannot transition to previous state"
            )
            return
        self.transition_to(self.state - 1)
        self.log.info("Transitioned to previous state:", self.state)

    def tick(self):
        # self.log.trace("Entering tick")
        if self.state == WallStakeState.DOCKED:
            self.gravitational_feedforward.kg = self.FEEDFORWARD_GAIN * -1
        else:
            self.gravitational_feedforward.kg = self.FEEDFORWARD_GAIN

        self.update_motor_voltage()

    def loop(self):
        # self.log.trace("Entering loop")
        while True:
            self.tick()
            time.sleep_ms(10)

    def at_setpoint(self):
        at_setpoint = self.pid.at_setpoint(self.POSITIONAL_TOLERANCE.to_revolutions())
        # self.log.debug("At setpoint:", at_setpoint)
        return at_setpoint
