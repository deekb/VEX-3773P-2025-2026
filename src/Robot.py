import VEXLib.Math.MathUtil as MathUtil
import VEXLib.Sensors.Controller
from AutonomousRoutines import AutonomousRoutines
from ConstantsV1 import *
from CornerMechanism import CornerMechanism
from Drivetrain import Drivetrain
from MobileGoalClamp import MobileGoalClamp
from ScoringMechanism import ScoringMechanism
from VEXLib.Kinematics import desaturate_wheel_speeds
from VEXLib.Robot.ScrollBufferedScreen import ScrollBufferedScreen
from VEXLib.Robot.TimedRobot import TimedRobot
from VEXLib.Util import time, pass_function
from VEXLib.Util.Logging import Logger
from WallStakeMechanism import WallStakeMechanism
from vex import *


class Robot(TimedRobot):
    def __init__(self, brain):
        super().__init__(brain)
        self.controller = VEXLib.Sensors.Controller.Controller(PRIMARY)
        self.drivetrain = Drivetrain([Motor(SmartPorts.FRONT_LEFT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, True),
                                      Motor(SmartPorts.MIDDLE_LEFT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, True),
                                      Motor(SmartPorts.REAR_LEFT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, True)],

                                     [Motor(SmartPorts.FRONT_RIGHT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, False),
                                      Motor(SmartPorts.MIDDLE_RIGHT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, False),
                                      Motor(SmartPorts.REAR_RIGHT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, False)], )

        self.screen = ScrollBufferedScreen()

        self.main_log = Logger(self.brain.sdcard, MAIN_LOG_FILENAME)

        self.user_preferences = DefaultPreferences
        self.mobile_goal_clamp = MobileGoalClamp(ThreeWirePorts.MOBILE_GOAL_CLAMP_PISTON)
        self.scoring_mechanism = ScoringMechanism(
            [Motor(SmartPorts.SCORING_ELEVEN_WATT_MOTOR, GearSetting.RATIO_18_1, False),
             Motor(SmartPorts.SCORING_FIVE_POINT_FIVE_WATT_MOTOR, GearSetting.RATIO_18_1, True)])
        self.wall_stake_mechanism = WallStakeMechanism(Motor(SmartPorts.WALL_STAKE_MOTOR, GearSetting.RATIO_36_1, True),
                                                       Limit(ThreeWirePorts.WALL_STAKE_CALIBRATION_LIMIT_SWITCH), )
        self.corner_mechanism = CornerMechanism(
            DigitalOut(ThreeWirePorts.DOINKER_PISTON)
        )
        self.animation_frame = 1
        self.autonomous_mappings = self.scan_autonomous_routines()

        self.autonomous = pass_function

    def scan_autonomous_routines(self):
        objects = AutonomousRoutines.__dict__
        routines = {}

        for name, _object in objects.items():
            if callable(_object) and not name.startswith("_"):
                # Ignore hidden objects or objects that can not be executed
                self.log_and_print("Discovered autonomous routine: " + str(name))
                routines[name] = _object
        return routines

    def log_and_print(self, *parts):
        message = " ".join(map(str, parts))
        self.screen.add_line(message)
        self.brain.screen.clear_screen()
        self.brain.screen.set_cursor(1, 1)
        for line in self.screen.get_screen_content():
            self.brain.screen.print(line)
            self.brain.screen.next_row()
        self.print_log.log(message)
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

    def on_driver_control(self):
        self.wall_stake_mechanism.motor.set_velocity(0, PERCENT)
        self.wall_stake_mechanism.motor.spin(FORWARD)

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

        self.log_and_print("Calibrating wall stake mechanism...")
        self.wall_stake_mechanism.calibrate()
        self.log_and_print("Calibrated wall stake mechanism successfully")
        self.controller.rumble("..")
        self.log_and_print("Selecting autonomous routine...")
        autonomous_routine = self.select_autonomous_routine()
        self.log_and_print("Selected autonomous routine:", autonomous_routine)

        drive_style = self.get_selection(["Dirk", "Derek"])
        self.log_and_print("Selected drive style:", drive_style)

        if drive_style == "Dirk":
            self.user_preferences = DirkPreferences
        elif drive_style == "Derek":
            self.user_preferences = DerekPreferences

        self.log_and_print("Set up user preferences:", drive_style)

        if isinstance(self.user_preferences, DirkPreferences):
            self.setup_dirk_preferences()
        elif isinstance(self.user_preferences, DerekPreferences):
            self.setup_derek_preferences()

    def driver_control_periodic(self):
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
        self.wall_stake_mechanism.tick()

    def setup_dirk_preferences(self):
        """Setup controller buttons for DirkPreferences."""
        self.controller.buttonX.pressed(self.trigger_restart)
        self.controller.buttonB.pressed(lambda: self.log_and_print("Toggling clamp") or self.mobile_goal_clamp.toggle_clamp)
        self.controller.buttonY.pressed(lambda: self.log_and_print("Toggling corner mechanism") or self.corner_mechanism.toggle_corner_mechanism)
        self.controller.buttonR1.pressed(lambda: self.log_and_print("Wall stake mechanism moving in") or self.wall_stake_mechanism.move_in)
        self.controller.buttonR1.released(lambda: self.log_and_print("Wall stake mechanism stopped") or self.wall_stake_mechanism.stop)
        self.controller.buttonL1.released(self.wall_stake_mechanism.stop)
        self.controller.buttonL2.pressed(self.scoring_mechanism.outtake)
        self.controller.buttonL2.released(self.scoring_mechanism.stop_motor)
        self.controller.buttonR2.pressed(self.scoring_mechanism.intake)
        self.controller.buttonR2.released(self.scoring_mechanism.stop_motor)
        self.controller.buttonDown.pressed(self.wall_stake_mechanism.dock)
        self.controller.buttonRight.pressed(self.wall_stake_mechanism.score)

    def setup_derek_preferences(self):
        """Setup controller buttons for DerekPreferences."""
        self.controller.buttonX.pressed(self.trigger_restart)
        self.controller.buttonB.pressed(self.mobile_goal_clamp.toggle_clamp)
        self.controller.buttonY.pressed(self.corner_mechanism.toggle_corner_mechanism)
        self.controller.buttonL1.pressed(self.scoring_mechanism.intake)
        self.controller.buttonL1.released(self.scoring_mechanism.stop_motor)
        self.controller.buttonL2.pressed(self.scoring_mechanism.outtake)
        self.controller.buttonL2.released(self.scoring_mechanism.stop_motor)
        self.controller.buttonR2.pressed(self.wall_stake_mechanism.move_in)
        self.controller.buttonR2.released(self.wall_stake_mechanism.stop)
        self.controller.buttonR1.pressed(self.wall_stake_mechanism.move_out)
        self.controller.buttonR1.released(self.wall_stake_mechanism.stop)
