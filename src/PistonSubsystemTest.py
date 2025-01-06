from Constants import ThreeWirePorts
from VEXLib.Subsystems.PistonSubsystem import PistonSubsystem


class MobileGoalClamp(PistonSubsystem):
    # Declare placeholders for autocompletion
    def clamp_mobile_goal(self):
        ...

    def release_mobile_goal(self):
        ...

    def toggle_clamp(self):
        ...

    def __init__(self):
        super().__init__(ThreeWirePorts.MOBILE_GOAL_CLAMP_PISTON,
                         True,
                         "Mobile Goal Clamp",
                         {
                             "extend": "clamp_mobile_goal",
                             "retract": "release_mobile_goal",
                             "toggle": "toggle_clamp"
                         })


instance = MobileGoalClamp()

instance.clamp_mobile_goal()
