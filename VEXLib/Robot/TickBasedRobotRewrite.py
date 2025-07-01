from vex import *
from VEXLib.Util import ContinuousTimer
from VEXLib.Robot.Constants import TARGET_TICK_DURATION_MS, WARNING_TICK_DURATION_MS
from VEXLib.Robot.RobotBase import RobotBase


class TickBasedRobot(RobotBase):
    """
    Combines a tick-based control system
    """

    def __init__(self, brain: Brain):
        super().__init__(brain)

        # Create a new competition object
        self._competition = Competition(self.on_driver_control, self.on_autonomous)

        # Tick-based control variables
        self.next_tick_time = ContinuousTimer.time_ms() + 1
        self._target_tick_duration_ms = TARGET_TICK_DURATION_MS
        self._warning_tick_duration_ms = WARNING_TICK_DURATION_MS

        self._current_time = ContinuousTimer.time_ms()
        self._last_tick_time = ContinuousTimer.time_ms()

    def start(self):
        self.on_setup()
        self._mainloop()

        self._handle_periodic_callbacks()

    def _mainloop(self):
        while True:
            current_time = self.brain.timer.system_high_res()
            if current_time >= self.next_tick_time:
                break
            self.tick()

    def _handle_periodic_callbacks(self):
        while True:
            now = ContinuousTimer.time_ms()
            print("NOW:" + str(now))
            print("NEXT:" + str(self.next_tick_time))
            if now >= self.next_tick_time:
                break
        if now > self.next_tick_time + (self._warning_tick_duration_ms - self._target_tick_duration_ms):
            time_overrun = now - self.next_tick_time
            print("PANIC: Scheduler tick overran target period by " + str(time_overrun) + " ms")
        self.next_tick_time += self._target_tick_duration_ms
