import VEXLib.Math.MathUtil as MathUtil
import VEXLib.Sensors.Controller
from AutonomousRoutines import AutonomousRoutines
from ConstantsV1 import *
from Drivetrain import Drivetrain
from VEXLib.Kinematics import desaturate_wheel_speeds
from VEXLib.Robot.ScrollBufferedScreen import ScrollBufferedScreen
from VEXLib.Robot.TimedRobot import TimedRobot
from VEXLib.Threading.BinarySemaphore import BinarySemaphore
from VEXLib.Util import time, pass_function
from VEXLib.Util.Logging import Logger
from MobileGoalClamp import MobileGoalClamp
from ScoringMechanism import ScoringMechanism
from vex import *


# noinspection DuplicatedCode
class Robot(TimedRobot):
    def __init__(self, brain):
        super().__init__(brain)
        self.controller = VEXLib.Sensors.Controller.Controller(PRIMARY)
        self.drivetrain = Drivetrain([Motor(Ports.PORT14, GearRatios.DRIVETRAIN, True),
                                      Motor(Ports.PORT13, GearRatios.DRIVETRAIN, True),
                                      Motor(Ports.PORT12, GearRatios.DRIVETRAIN, False)],

                                     [Motor(Ports.PORT15, GearRatios.DRIVETRAIN, False),
                                      Motor(Ports.PORT16, GearRatios.DRIVETRAIN, False),
                                      Motor(Ports.PORT17, GearRatios.DRIVETRAIN, True)])

        # self._warning_tick_duration_ms = 100_000

        self.screen = ScrollBufferedScreen()
        self.render_lock = BinarySemaphore()

        self.main_log = Logger(self.brain.sdcard, MAIN_LOG_FILENAME)

        self.mobile_goal_clamp = MobileGoalClamp(ThreeWirePorts.MOBILE_GOAL_CLAMP_PISTON)
        self.scoring_mechanism = ScoringMechanism(
            [Motor(Ports.PORT1, GearSetting.RATIO_18_1, False),
             Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)])

        self.user_preferences = DefaultPreferences
        self.autonomous_mappings = self.scan_autonomous_routines()
        self.autonomous = pass_function

    def scan_autonomous_routines(self):
        objects = AutonomousRoutines.__dict__
        routines = {}
        self.log_and_print("Discovering autonomous routines...")

        for name, _object in objects.items():
            self.log_and_print("Checking object:", name)
            if not name.startswith("_"):
                # Ignore hidden objects or objects that can not be executed
                self.log_and_print("Discovered autonomous routine: " + str(name))
                routines[name] = _object
        return routines

    def log_and_print(self, *parts):
        message = " ".join(map(str, parts))
        self.screen.add_line(message)
        self.render_lock.acquire()
        self.brain.screen.clear_screen()
        self.brain.screen.set_cursor(1, 1)
        for line in self.screen.get_screen_content():
            self.brain.screen.print(line)
            self.brain.screen.next_row()
        self.render_lock.release()
        self.main_log.log(message)
        print(message)

    def debug_wait(self):
        while not self.controller.buttonA.pressing():
            pass
        while self.controller.buttonA.pressing():
            pass

    def on_autonomous(self):
        self.log_and_print("Executing chosen autonomous routine:", str(self.autonomous))
        self.autonomous(self)

    def on_enable(self):
        self.log_and_print("on_enable called: resetting drivetrain")
        self.drivetrain.reset()

    def get_selection(self, options):
        """
        Allows the user to navigate through a list of options and select one using specified controls.
        The function implements a loop to display and navigate through options using a controller.
        It reacts to button presses to modify the selection index or make a selection.

        Args:
            options (list): A list of options from which the user can select.

        Returns:
            Any: The selected option from the list.
        """
        selection_index = 0

        while True:
            self.controller.screen.clear_screen()
            self.controller.screen.set_cursor(1, 1)
            self.controller.screen.print(options[selection_index])
            while not (
                    self.controller.buttonRight.pressing() or self.controller.buttonLeft.pressing() or self.controller.buttonA.pressing()):
                time.sleep_ms(5)

            if self.controller.buttonA.pressing():
                break

            if self.controller.buttonRight.pressing():
                selection_index += 1
            elif self.controller.buttonLeft.pressing():
                selection_index -= 1

            while self.controller.buttonRight.pressing() or self.controller.buttonLeft.pressing():
                time.sleep_ms(5)

            if selection_index < 0:
                selection_index = 0
            elif selection_index >= len(options) - 1:
                selection_index = len(options) - 1
        while self.controller.buttonA.pressing():
            time.sleep_ms(5)

        return options[selection_index]

    def select_autonomous_routine(self):
        self.log_and_print("Starting autonomous routine selection")
        autonomous_type = self.get_selection(["red", "blue", "skills_alliance_stake"])
        if autonomous_type == "skills_alliance_stake":
            self.drivetrain.set_angles_inverted(False)
            self.autonomous = AutonomousRoutines.skills_alliance_stake
            self.log_and_print("Skills routine chosen:", autonomous_type)
            return autonomous_type

        auto = self.get_selection(list(self.autonomous_mappings.keys()))

        self.drivetrain.set_angles_inverted(autonomous_type == "blue")
        self.autonomous = self.autonomous_mappings[auto]

        return autonomous_type + " " + auto

    def on_setup(self):
        self.drivetrain.inertial.calibrate()
        self.log_and_print("Calibrating inertial sensor...")
        while self.drivetrain.inertial.is_calibrating():
            time.sleep_ms(5)
        self.log_and_print("Calibrated inertial sensor successfully")
        self.controller.rumble("..")
        self.log_and_print("Selecting autonomous routine...")
        autonomous_routine = self.select_autonomous_routine()
        self.log_and_print("Selected autonomous routine:", autonomous_routine)

        drive_style = self.get_selection(["Dirk", "Derek"])
        self.log_and_print("Selected drive style:", drive_style)

        if drive_style == "Dirk":
            self.user_preferences = DirkPreferences
            self.setup_dirk_preferences()
        elif drive_style == "Derek":
            self.user_preferences = DerekPreferences
            self.setup_derek_preferences()

        self.log_and_print("Set up user preferences:", drive_style)

        self.log_and_print("Setup complete")
        # self.log_and_print("Measuring drivetrain properties...")
        # self.log_and_print("Left drivetrain properties:", self.drivetrain.ramp_voltage_and_collect_data(self.drivetrain.left_motors))
        # self.log_and_print("Right drivetrain properties:", self.drivetrain.ramp_voltage_and_collect_data(self.drivetrain.right_motors))

    def periodic(self):
        self.render_lock.acquire()
        self.brain.screen.render()
        self.render_lock.release()

    def driver_control_periodic(self):
        # if self.controller.buttonA.pressing():
        #     start_time = time.time()
        #     start_rotation = self.drivetrain.odometry.get_rotation().to_revolutions()
        #     self.drivetrain.set_voltage(12, -12)
        #     while abs(start_rotation - self.drivetrain.odometry.get_rotation().to_revolutions()) < 1:
        #         self.drivetrain.update_odometry()
        #     self.drivetrain.set_voltage(0, 0)
        #     self.log_and_print("Time taken to rotate 1 revolution:", time.time() - start_time)

        left_speed = right_speed = 0
        if self.user_preferences.CONTROLLER_BINDINGS_STYLE == ControlStyles.TANK:
            left_speed = self.controller.left_stick_y()
            right_speed = self.controller.right_stick_y()

            left_speed = MathUtil.apply_deadband(left_speed)
            right_speed = MathUtil.apply_deadband(right_speed)
        elif self.user_preferences.CONTROLLER_BINDINGS_STYLE in [ControlStyles.ARCADE, ControlStyles.SPLIT_ARCADE]:
            forward_speed = turn_speed = 0
            forward_speed = self.controller.left_stick_y()
            if self.user_preferences.CONTROLLER_BINDINGS_STYLE == ControlStyles.ARCADE:
                turn_speed = self.controller.left_stick_x()
            elif self.user_preferences.CONTROLLER_BINDINGS_STYLE == ControlStyles.SPLIT_ARCADE:
                turn_speed = self.controller.right_stick_x()

            forward_speed = MathUtil.apply_deadband(forward_speed)
            turn_speed = -MathUtil.apply_deadband(turn_speed)

            left_speed = forward_speed - turn_speed
            right_speed = forward_speed + turn_speed
        else:
            self.log_and_print("Invalid controller bindings style:", self.user_preferences.CONTROLLER_BINDINGS_STYLE)

        left_speed, right_speed = desaturate_wheel_speeds([left_speed, right_speed])

        left_speed = MathUtil.cubic_filter(left_speed, linearity=self.user_preferences.CUBIC_FILTER_LINEARITY)
        right_speed = MathUtil.cubic_filter(right_speed, linearity=self.user_preferences.CUBIC_FILTER_LINEARITY)

        # self.log_and_print("Updating drivetrain voltages - Left:", left_speed, "Right:", right_speed)
        self.drivetrain.set_voltage(left_speed * self.user_preferences.MAX_MOTOR_VOLTAGE,
                                    right_speed * self.user_preferences.MAX_MOTOR_VOLTAGE)

        self.drivetrain.update_odometry()

    def setup_dirk_preferences(self):
        """Setup controller buttons for DirkPreferences."""
        self.log_and_print("Setting up Dirk Preferences")
        self.controller.buttonX.pressed(self.trigger_restart)
        self.controller.buttonB.pressed(lambda: self.log_and_print("Toggling clamp") or self.mobile_goal_clamp.toggle_clamp)
        self.controller.buttonL2.pressed(self.scoring_mechanism.outtake)
        self.controller.buttonL2.released(self.scoring_mechanism.stop_motor)
        self.controller.buttonR2.pressed(self.scoring_mechanism.intake)
        self.controller.buttonR2.released(self.scoring_mechanism.stop_motor)

    def setup_derek_preferences(self):
        """Setup controller buttons for DerekPreferences."""
        self.log_and_print("Setting up Derek Preferences")
        self.controller.buttonX.pressed(self.trigger_restart)
        self.controller.buttonB.pressed(lambda: self.log_and_print("Toggling clamp") or self.mobile_goal_clamp.toggle_clamp)
        self.controller.buttonL1.pressed(self.scoring_mechanism.intake)
        self.controller.buttonL1.released(self.scoring_mechanism.stop_motor)
        self.controller.buttonL2.pressed(self.scoring_mechanism.outtake)
        self.controller.buttonL2.released(self.scoring_mechanism.stop_motor)