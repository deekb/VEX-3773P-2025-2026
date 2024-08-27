import Constants
from vex import DigitalOut


class MobileGoalClamp:
    def __init__(self):
        self.mobile_goal_clamp_piston = DigitalOut(Constants.ThreeWirePorts.MOBILE_GOAL_CLAMP_PISTON)
        self.mobile_goal_clamp_state = False

    def _update_state(self):
        self.mobile_goal_clamp_piston.set(self.mobile_goal_clamp_state)

    def clamp_mobile_goal(self):
        self.mobile_goal_clamp_state = True
        self._update_state()

    def release_mobile_goal(self):
        self.mobile_goal_clamp_state = False
        self._update_state()

    def toggle_clamp(self):
        self.mobile_goal_clamp_state = not self.mobile_goal_clamp_state
        self._update_state()
