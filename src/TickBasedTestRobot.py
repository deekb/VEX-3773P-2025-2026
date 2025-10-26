from VEXLib.Robot.TimedRobot import TimedRobot
from VEXLib.Sensors.Controller import Controller
from VEXLib.Util.time import wait_until_not
from vex import Color


class Robot(TimedRobot):
    def __init__(self, brain):
        super().__init__(brain)
        self.controller = Controller()
        self.x_data = []
        self.y_data = []
        self.time_data = []
        self.collecting_data = False

    """Instant callbacks"""

    def on_enable(self):
        """
        Run whenever the robot is enabled while in either autonomous or driver control mode
        This means that this method is also executed when the robot is enabled and is switched from autonomous to driver control mode or vice versa
        """
        self.x_data = []
        self.y_data = []
        self.time_data = []
        # print("on_enable")

    def save_controller_samples(self):
        with open("logs/controller_x.txt", "w") as f:
            for line in self.x_data:
                f.write(str(line) + "\n")
        with open("logs/controller_y.txt", "w") as f:
            for line in self.y_data:
                f.write(str(line) + "\n")
        with open("logs/controller_time.txt", "w") as f:
            for line in self.time_data:
                f.write(str(line) + "\n")

    def on_disable(self):
        """
        Run whenever the robot is disabled while in either autonomous or driver control mode
        This means that this method is also executed when the robot is disabled and is switched from autonomous to driver control mode or vice versa
        """
        self.save_controller_samples()
        # print("on_disable")

    def on_driver_control(self):
        """
        Run whenever the robot is enabled while in driver control mode or is enabled and switches from autonomous to driver control
        """
        # print("on_driver_control")

    def on_driver_control_disable(self):
        """
        Run whenever the robot is disabled while in driver control mode or is disabled and switches from autonomous to driver control
        """
        # print("on_driver_control_disable")

    def on_autonomous(self):
        """
        Run whenever the robot is enabled while in autonomous mode or is enabled and switches from driver control to autonomous
        """
        # print("on_autonomous")

    def on_autonomous_disable(self):
        """
        Run whenever the robot is disabled while in autonomous mode or is disabled and switches from driver control to autonomous
        """
        # print("on_autonomous_disable")

    """Periodic callbacks"""

    def periodic(self):
        """
        Run periodically approximately 50 times a second (20ms between ticks) no matter the competition mode
        """
        # print("periodic")
        print("LX: {}".format(self.controller.left_stick_x()))
        print("LY: {}".format(self.controller.left_stick_y()))
        print("")
        print("RX: {}".format(self.controller.right_stick_x()))
        print("RY: {}".format(self.controller.right_stick_y()))

    def driver_control_periodic(self):
        """
        Run periodically approximately 50 times a second (20ms between ticks) while driver control is enabled
        """
        # print("driver_control_periodic")

    def autonomous_periodic(self):
        """
        Run periodically approximately 50 times a second (20ms between ticks) while autonomous is enabled
        """
        # print("autonomous_periodic")

    def enabled_periodic(self):
        """
        Run periodically approximately 50 times a second (20ms between ticks) while the robot is enabled in either autonomous or driver control mode
        """
        if self.controller.buttonA.pressing():
            wait_until_not(self.controller.buttonA.pressing)
            self.collecting_data = True
            self.brain.screen.set_fill_color(Color.GREEN)
            self.brain.screen.draw_rectangle(0, 0, 480, 240)
        if self.collecting_data:
            try:
                self.x_data.append(self.controller.left_stick_x())
                self.y_data.append(self.controller.left_stick_y())
                self.time_data.append(self.time_since_enable())
            except MemoryError:
                self.brain.screen.print("Memory Overflow, saving existing samples")
                self.save_controller_samples()
                self.collecting_data = False
                self.brain.screen.set_fill_color(Color.GREEN)
                self.brain.screen.draw_rectangle(0, 0, 480, 240)

        # print("enabled_periodic")

    def disabled_periodic(self):
        """
        Run periodically approximately 50 times a second (20ms between ticks) while the robot is disabled in either autonomous or driver control mode
        """
        # print("disabled_periodic")
