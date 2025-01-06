from vex import *
from VEXLib.Util import ContinuousTimer, pass_function
from VEXLib.Robot.Constants import DRIVER_CONTROL, AUTONOMOUS_CONTROL, TARGET_TICK_DURATION_MS, \
    WARNING_TICK_DURATION_MS, ENABLED, DISABLED
from VEXLib.Robot.RobotBase import RobotBase
from collections import namedtuple

GameState = namedtuple('GameState', ['mode', 'enabled'])

DRIVER_CONTROL_ENABLED = GameState(DRIVER_CONTROL, ENABLED)
DRIVER_CONTROL_DISABLED = GameState(DRIVER_CONTROL, DISABLED)
AUTONOMOUS_CONTROL_ENABLED = GameState(AUTONOMOUS_CONTROL, ENABLED)
AUTONOMOUS_CONTROL_DISABLED = GameState(AUTONOMOUS_CONTROL, DISABLED)


class TickBasedRobot(RobotBase):
    """
    Combines a tick-based control system with state transitions for driver and autonomous control.
    """

    def __init__(self, brain: Brain):
        super().__init__(brain)

        # Create a new competition object
        self._competition = Competition(pass_function, self.on_autonomous)

        self.state = DRIVER_CONTROL_DISABLED  # Initial state
        self.transitions = {DRIVER_CONTROL_DISABLED: self._from_driver_control_disabled,
                            AUTONOMOUS_CONTROL_DISABLED: self._from_autonomous_control_disabled,
                            DRIVER_CONTROL_ENABLED: self._from_driver_control_enabled,
                            AUTONOMOUS_CONTROL_ENABLED: self._from_autonomous_control_enabled,
                            }

        # Tick-based control variables
        self.next_tick_time = ContinuousTimer.time_ms() + 1
        self._target_tick_duration_ms = TARGET_TICK_DURATION_MS
        self._warning_tick_duration_ms = WARNING_TICK_DURATION_MS

        self.restart_requested = False

        self._last_enable_time = self._last_disable_time = ContinuousTimer.time()

        self._current_time = ContinuousTimer.time_ms()
        self._last_tick_time = ContinuousTimer.time_ms()

    def control_loop(self):
        self._handle_periodic_callbacks_internal()

    def start(self):
        self.on_setup()
        self._mainloop()

    def trigger_restart(self):
        self.restart_requested = True

    def _update_state(self):
        if self._competition.is_autonomous():
            mode = AUTONOMOUS_CONTROL
        else:
            mode = DRIVER_CONTROL

        enabled = self._competition.is_enabled()

        return GameState(mode, enabled)

    def _tick(self):
        new_state = self._update_state()

        if new_state != self.state:
            print("New state != Current state")
            print("Transitioning from " + str(self.state) + " to " + str(new_state))
            self.transition_to(new_state)

        self._handle_periodic_callbacks()

    def _mainloop(self):
        while True:
            self._tick()

    def _handle_periodic_callbacks(self):
        while True:
            now = ContinuousTimer.time_ms()
            if now >= self.next_tick_time:
                break
        self.control_loop()
        if now > self.next_tick_time + (self._warning_tick_duration_ms - self._target_tick_duration_ms):
            time_overrun = now - self.next_tick_time
            print("PANIC: Scheduler tick overran target period by " + str(time_overrun) + " ms")
        self.next_tick_time += self._target_tick_duration_ms

    def _handle_periodic_callbacks_internal(self):
        if self.state.enabled:
            if self.state.mode == DRIVER_CONTROL:
                self.driver_control_periodic()
            elif self.state.mode == AUTONOMOUS_CONTROL:
                self.autonomous_periodic()
            self.enabled_periodic()
        else:
            self.disabled_periodic()
        self.periodic()
        self._last_tick_time = ContinuousTimer.time_ms()

    def transition_to(self, new_state: GameState):
        if self.state == new_state:
            print("Already in state: " + str(self.state) + ". No transition needed.")
            return

        if new_state.enabled:
            self.on_enable()
        else:
            self.on_disable()

        # The inspection doesn't seem to understand that this is a function pulled from a dictionary
        # noinspection PyArgumentList
        self.transitions[self.state](new_state)

        self.state = new_state

    def _from_driver_control_disabled(self, new_state: GameState):
        if new_state == DRIVER_CONTROL_ENABLED:
            self.on_driver_control()
        elif new_state == AUTONOMOUS_CONTROL_ENABLED:
            self.on_autonomous()

    def _from_autonomous_control_disabled(self, new_state: GameState):
        if new_state == AUTONOMOUS_CONTROL_ENABLED:
            # self.on_autonomous()
            pass
        elif new_state == DRIVER_CONTROL_ENABLED:
            self.on_driver_control()

    def _from_driver_control_enabled(self, new_state: GameState):
        if new_state == DRIVER_CONTROL_DISABLED:
            self.on_driver_control_disable()
        elif new_state == AUTONOMOUS_CONTROL_DISABLED:
            self.on_driver_control_disable()
        elif new_state == AUTONOMOUS_CONTROL_ENABLED:
            self.on_driver_control_disable()
            self.on_disable()
            # self.on_autonomous()

    def _from_autonomous_control_enabled(self, new_state: GameState):
        if new_state == DRIVER_CONTROL_DISABLED:
            self.on_autonomous_disable()
        elif new_state == DRIVER_CONTROL_ENABLED:
            self.on_autonomous_disable()
            self.on_disable()
            self.on_driver_control()
        elif new_state == AUTONOMOUS_CONTROL_DISABLED:
            self.on_autonomous_disable()

    """Polling methods"""

    def is_enabled(self):
        """
        Get whether the robot is currently enabled
        """
        return self.state.enabled == ENABLED

    def is_disabled(self):
        """
        Get whether the robot is currently disabled
        """
        return self.state.enabled == ENABLED.enabled == DISABLED

    def is_driver_control(self):
        """
        Get whether the robot is currently in driver control mode
        """
        return self.state.mode == DRIVER_CONTROL

    def is_autonomous_control(self):
        """
        Get whether the robot is currently in autonomous control mode
        """
        return self.state.mode == AUTONOMOUS_CONTROL
