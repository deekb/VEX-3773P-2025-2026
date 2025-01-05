from vex import *
from VEXLib.Util import time, pass_function
from VEXLib.Robot.Constants import *
from VEXLib.Robot.RobotBase import RobotBase


class States:
    AUTONOMOUS_DISABLE = 1
    AUTONOMOUS_ENABLE = 2
    DRIVER_CONTROL_DISABLE = 3
    DRIVER_CONTROL_ENABLE = 4


class TickBasedRobot(RobotBase):
    def __init__(self, brain: Brain):
        super().__init__(brain)

        # Create a new competition object
        # and initialize the callbacks for driver and autonomous control to a "pass function".
        # This means that the robot will not automatically run code when it is enabled or disabled
        # We do this because we would like to handle running the state machine and callbacks ourselves.
        # This allows for more predictable behaviors and the injection of additional functionality
        self._competition = Competition(
            pass_function, pass_function
        )

        # Schedule the first update to happen 1 ms after startup
        self.next_tick_time = time.time_ms() + 1
        # self.f = open("/dev/port2", "wb")

        self._target_tick_duration_ms = TARGET_TICK_DURATION_MS
        self._warning_tick_duration_ms = WARNING_TICK_DURATION_MS

        self._enabled = True
        self.restart_requested = False
        self._previous_enabled = self._enabled
        self._update_enabled()

        self._last_enable_time = self._last_disable_time = 0.0

        if self._enabled:
            self._last_enable_time = time.time_ms()
        else:
            self._last_disable_time = time.time_ms()

        self._mode = DRIVER_CONTROL
        self._previous_mode = self._mode
        self._update_mode()

        self._current_time = None
        self._update_time()
        self._last_tick_time = self._current_time

    def control_loop(self):
        # self.f.write(b"\x0f")
        self._handle_periodic_callbacks_internal()
        # self.f.write(b"\xf0")

    def start(self):
        # Run the user-defined setup method
        self.setup()
        # Start the mainloop, this handles calling periodic and instant callbacks
        self._mainloop()

    def trigger_restart(self):
        self.restart_requested = True

    def _update_time(self):
        self._current_time = time.time_ms()

    def _update_enabled(self):
        if self._competition.is_field_control():
            self._enabled = self._competition.is_enabled()
        elif self._competition.is_competition_switch():
            self._enabled = self._competition.is_enabled()
        else:
            # There is nothing controlling the mode, so the default is driver control enabled
            self._enabled = True

    def _update_mode(self):
        if self._competition.is_field_control():
            self._mode = AUTONOMOUS_CONTROL if self._competition.is_autonomous() else DRIVER_CONTROL
        elif self._competition.is_competition_switch():
            self._mode = AUTONOMOUS_CONTROL if self._competition.is_autonomous() else DRIVER_CONTROL
        else:
            # There is nothing controlling the mode, so the default is driver control enabled
            self._mode = DRIVER_CONTROL

    def _update_state(self):
        self._update_enabled()
        self._update_mode()
        self._update_time()

    def _mainloop(self):
        """
        Handle internal competition state logic
        """
        self._update_state()
        self._handle_instant_callbacks()  # Force a manual call to instant callbacks for initial setup
        while True:
            self._update_state()

            if self._mode != self._previous_mode or self._enabled != self._previous_enabled:
                print("IC:RERUN")
                # If the mode or enabled state has changed since last update
                # then run the appropriate instant callbacks
                self._handle_instant_callbacks()
            self._previous_enabled = self._enabled
            self._previous_mode = self._mode

            self._handle_periodic_callbacks()  # Run the appropriate periodic callbacks every update

    def get_tick_time(self):
        return self._current_time

    def setup(self):
        """
        Run when the program is started to set up the robot (autonomous selection screen, calibration, etc.)
        This method is run before all other methods (on_enable, periodic, disabled_periodic, etc.) and blocks execution until it finishes.
        """

    def _handle_instant_callbacks(self):
        self._handle_disable_callbacks()
        self._handle_enable_callbacks()

    # def _handle_enable_callbacks(self):
    #     """
    #     Handle callbacks when the robot is enabled
    #     """
    #     self._last_enable_time = time.time_ms()
    #     self.on_enable()
    #     if self.is_autonomous_control():
    #         self.on_autonomous()
    #     elif self.is_driver_control():
    #         self.on_driver_control()
    #
    # def _handle_disable_callbacks(self):
    #     """
    #     Handle callbacks when the robot is disabled
    #     """
    #     self._last_disable_time = time.time_ms()
    #     self.on_disable()
    #     if self._previous_mode == AUTONOMOUS_MODE:
    #         self.on_autonomous_disable()
    #     elif self._previous_mode == DRIVER_CONTROL_MODE:
    #         self.on_driver_control_disable()

    def _handle_enable_callbacks(self):
        """
        Handle callbacks when the robot is enabled
        """
        self._last_enable_time = time.time_ms()
        # if self._previous_enabled == False and self._previous_mode == DRIVER_CONTROL_MODE:

    def _handle_disable_callbacks(self):
        """
        Handle callbacks when the robot is disabled
        """
        self._last_disable_time = time.time_ms()

    def _handle_periodic_callbacks(self):
        """
        Handle periodic callbacks
        """

        while True:
            now = time.time_ms()
            if now >= self.next_tick_time:
                break
        self.control_loop()
        if now > self.next_tick_time + (self._warning_tick_duration_ms - self._target_tick_duration_ms):
            time_overrun = now - self.next_tick_time
            message = "PANIC: Scheduler tick overran period by " + str(time_overrun) + " ms"
            print(message)
        self.next_tick_time += self._target_tick_duration_ms

    def _handle_periodic_callbacks_internal(self):
        """
        Handle the internal logic for periodic callbacks
        """
        if self._enabled:
            if self.is_driver_control():
                self.driver_control_periodic()
            elif self.is_autonomous_control():
                self.autonomous_periodic()
            self.enabled_periodic()
        else:
            self.disabled_periodic()

        self.periodic()
        self._last_tick_time = self._current_time

    """Polling methods"""

    def is_enabled(self):
        """
        Get whether the robot is currently enabled
        """
        return self._enabled

    def is_disabled(self):
        """
        Get whether the robot is currently disabled
        """
        return not self._enabled

    def is_driver_control(self):
        """
        Get whether the robot is currently in driver control mode
        """
        return self._mode == DRIVER_CONTROL

    def is_autonomous_control(self):
        """
        Get whether the robot is currently in autonomous control mode
        """
        return self._mode == AUTONOMOUS_CONTROL
