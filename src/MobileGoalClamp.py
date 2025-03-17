from VEXLib.Util.Logging import Logger
from vex import DigitalOut, Brain

mobile_goal_clamp_log = Logger(Brain().sdcard, Brain().screen, "mobile_goal_clamp")


class MobileGoalClamp:
    def __init__(self, piston_port):
        self.mobile_goal_clamp_piston = DigitalOut(piston_port)
        self.mobile_goal_clamp_state = False
        self.log = mobile_goal_clamp_log

    def _update_state(self):
        self.log.trace("_update_state: setting state to {}".format(self.mobile_goal_clamp_state))
        self.mobile_goal_clamp_piston.set(self.mobile_goal_clamp_state)

    def clamp_mobile_goal(self):
        self.log.trace("Clamping mobile goal")
        self.mobile_goal_clamp_state = True
        self._update_state()

    def release_mobile_goal(self):
        self.log.trace("Releasing mobile goal")
        self.mobile_goal_clamp_state = False
        self._update_state()

    def toggle_clamp(self):
        self.log.trace("Toggling clamp from {} to {}".format(self.mobile_goal_clamp_state, not self.mobile_goal_clamp_state))
        self.mobile_goal_clamp_state = not self.mobile_goal_clamp_state
        self._update_state()
