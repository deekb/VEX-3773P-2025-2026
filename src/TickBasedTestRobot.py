from VEXLib.Robot.TickBasedRobot import TickBasedRobot


class Robot(TickBasedRobot):
    """
    This is the basic representation of a robot
    It has methods to be called when it is enabled and disabled
    """

    def __init__(self, brain):
        super().__init__(brain)

    """Instant callbacks"""

    def on_enable(self):
        """
        Run whenever the robot is enabled while in either autonomous or driver control mode
        This means that this method is also executed when the robot is enabled and is switched from autonomous to driver control mode or vice versa
        """
        print("on_enable")

    def on_disable(self):
        """
        Run whenever the robot is disabled while in either autonomous or driver control mode
        This means that this method is also executed when the robot is disabled and is switched from autonomous to driver control mode or vice versa
        """
        print("on_disable")

    def on_driver_control(self):
        """
        Run whenever the robot is enabled while in driver control mode or is enabled and switches from autonomous to driver control
        """
        print("on_driver_control")

    def on_driver_control_disable(self):
        """
        Run whenever the robot is disabled while in driver control mode or is disabled and switches from autonomous to driver control
        """
        print("on_driver_control_disable")

    def on_autonomous(self):
        """
        Run whenever the robot is enabled while in autonomous mode or is enabled and switches from driver control to autonomous
        """
        print("on_autonomous")

    def on_autonomous_disable(self):
        """
        Run whenever the robot is disabled while in autonomous mode or is disabled and switches from driver control to autonomous
        """
        print("on_autonomous_disable")

    """Periodic callbacks"""

    def periodic(self):
        """
        Run periodically approximately 50 times a second (20ms between ticks) no matter the competition mode
        """
        print("periodic")

    def driver_control_periodic(self):
        """
        Run periodically approximately 50 times a second (20ms between ticks) while driver control is enabled
        """
        print("driver_control_periodic")

    def autonomous_periodic(self):
        """
        Run periodically approximately 50 times a second (20ms between ticks) while autonomous is enabled
        """
        print("autonomous_periodic")

    def enabled_periodic(self):
        """
        Run periodically approximately 50 times a second (20ms between ticks) while the robot is enabled in either autonomous or driver control mode
        """
        print("enabled_periodic")

    def disabled_periodic(self):
        """
        Run periodically approximately 50 times a second (20ms between ticks) while the robot is disabled in either autonomous or driver control mode
        """
        print("disabled_periodic")
