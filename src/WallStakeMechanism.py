from Constants import WallStakeMechanismProperties
from VEXLib.Algorithms.GravitationalFeedforward import GravitationalFeedforward
from VEXLib.Algorithms.PID import PIDController
from VEXLib.Geometry.Rotation2d import Rotation2d
import VEXLib.Math.MathUtil as MathUtil
from vex import FORWARD, DEGREES, VOLT, Rotation, Thread


class WallStakeState:
    DOCKED = 1
    LOADING = 2
    HIGH_SCORING = 3
    LOW_SCORING = 4


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
            motor (vex.Motor): The motor controlling the wall stake mechanism.
            rotation_sensor (vex.Rotation): The rotation sensor used to measure the mechanism's position.
        """

        self.rotation_sensor = rotation_sensor
        self.motor = motor

        self.PID_TUNINGS = WallStakeMechanismProperties.PID_TUNINGS
        self.FEEDFORWARD_TUNINGS = WallStakeMechanismProperties.FEEDFORWARD_TUNINGS
        self.DOCKED_POSITION = WallStakeMechanismProperties.DOCKED_POSITION
        self.DOCKED_TOLERANCE = WallStakeMechanismProperties.DOCKED_TOLERANCE
        self.LOADING_POSITION = WallStakeMechanismProperties.LOADING_POSITION
        self.HIGH_SCORING_POSITION = WallStakeMechanismProperties.HIGH_SCORING_POSITION
        self.LOW_SCORING_POSITION = WallStakeMechanismProperties.LOW_SCORING_POSITION
        self.UPRIGHT_POSITION = WallStakeMechanismProperties.UPRIGHT_POSITION

        self.gravitational_feedforward = GravitationalFeedforward(self.FEEDFORWARD_TUNINGS["kg"])
        self.pid = PIDController(self.PID_TUNINGS["kp"], self.PID_TUNINGS["ki"], self.PID_TUNINGS["kd"])

        self.state = WallStakeState.DOCKED
        # Call transition_to to ensure we are really in the initial state
        self.transition_to(self.state)
        self.tick_thread = Thread(self.loop)

    def update_motor_voltage(self):
        current_rotation = Rotation2d.from_degrees(self.rotation_sensor.position(DEGREES))
        feedforward_output = self.gravitational_feedforward.update(current_rotation.to_degrees())
        pid_output = self.pid.update(current_rotation.normalize().to_revolutions())

        if self.state == WallStakeState.DOCKED and MathUtil.is_near(self.DOCKED_POSITION.to_revolutions(), current_rotation.to_revolutions(), self.DOCKED_TOLERANCE.to_revolutions()):
            self.motor.spin(FORWARD, 0, VOLT)
            return

        self.motor.spin(FORWARD, feedforward_output - pid_output, VOLT)

    def transition_to(self, new_state):
        if new_state == WallStakeState.DOCKED:
            print("Transitioning to Docked")
            self.pid.setpoint = self.DOCKED_POSITION.to_revolutions()
        elif new_state == WallStakeState.LOADING:
            print("Transitioning to Loading")
            self.pid.setpoint = self.LOADING_POSITION.to_revolutions()
        elif new_state == WallStakeState.HIGH_SCORING:
            print("Transitioning to High Scoring")
            self.pid.setpoint = self.HIGH_SCORING_POSITION.to_revolutions()
        elif new_state == WallStakeState.LOW_SCORING:
            print("Transitioning to Low Scoring")
            self.pid.setpoint = self.LOW_SCORING_POSITION.to_revolutions()

        self.state = new_state

    def next_state(self):
        if self.state == 4:
            return
        self.transition_to(self.state + 1)

    def previous_state(self):
        if self.state == 1:
            return
        self.transition_to(self.state - 1)

    def tick(self):
        if self.state == WallStakeState.DOCKED:
            self.gravitational_feedforward.kg = self.FEEDFORWARD_TUNINGS["kg"] * -1
        else:
            self.gravitational_feedforward.kg = self.FEEDFORWARD_TUNINGS["kg"]

        self.update_motor_voltage()

    def loop(self):
        while True:
            self.tick()
