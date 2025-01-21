import AutonomousRoutines
import VEXLib.Math.MathUtil as MathUtil
import VEXLib.Sensors.Controller
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
        self.print_log = Logger(self.brain.sdcard, PRINT_LOG_FILENAME)
        self.odometry_log = Logger(self.brain.sdcard, ODOMETRY_LOG_FILENAME)
        self.competition_state_log = Logger(self.brain.sdcard, COMPETITION_LOG_FILENAME)

        for log in [self.main_log, self.print_log, self.odometry_log, self.competition_state_log]:
            self.log_and_print("Log initialized for", log)

        self.user_preferences = DefaultPreferences
        self.mobile_goal_clamp = MobileGoalClamp(ThreeWirePorts.MOBILE_GOAL_CLAMP_PISTON)
        self.scoring_mechanism = ScoringMechanism(
            [Motor(SmartPorts.SCORING_ELEVEN_WATT_MOTOR, GearSetting.RATIO_18_1, False),
             Motor(SmartPorts.SCORING_FIVE_POINT_FIVE_WATT_MOTOR, GearSetting.RATIO_18_1, True)])
        self.wall_stake_mechanism = WallStakeMechanism()
        self.corner_mechanism = CornerMechanism()
        self.animation_frame = 1
        self.autonomous_mappings = {"negative_4_rings_and_touch": AutonomousRoutines.negative_4_rings_and_touch,
                                    "negative": AutonomousRoutines.negative,
                                    "square_test": AutonomousRoutines.test_autonomous,
                                    "positive": AutonomousRoutines.positive, "win_point": AutonomousRoutines.win_point,
                                    "forwards": AutonomousRoutines.drive_forwards,
                                    "positive_WP": AutonomousRoutines.positive_win_point,
                                    "positive_2_mobile_goal": AutonomousRoutines.positive_2_mobile_goal, }

        self.autonomous = pass_function

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
            button_release_delay = 5
            time.sleep_ms(button_release_delay)

        return options[selection_index]

    def select_autonomous_routine(self):
        self.log_and_print("Starting autonomous routine selection")
        color = self.get_selection(["red", "blue", "skills_alliance_stake"])
        if color == "skills_alliance_stake":
            self.drivetrain.set_angles_inverted(False)
            self.autonomous = AutonomousRoutines.skills_alliance_stake
            self.log_and_print("Skills routine chosen:", color)
            return color

        auto = self.get_selection(list(self.autonomous_mappings.keys()))

        self.drivetrain.set_angles_inverted(color == "blue")
        self.autonomous = self.autonomous_mappings[auto]

        return color + " " + auto

    @staticmethod
    def zpad_left(x, n):
        return "0" * (n - len(str(x))) + str(x)

    def on_setup(self):
        self.drivetrain.inertial.calibrate()
        self.log_and_print("Calibrating inertial sensor...")
        while self.drivetrain.inertial.is_calibrating():
            time.sleep_ms(5)
        self.log_and_print("Calibrated inertial sensor successfully")

        self.wall_stake_mechanism.calibrate()
        self.controller.rumble("..")
        autonomous_routine = self.select_autonomous_routine()
        self.log_and_print("Selected autonomous routine:", autonomous_routine)

        drive_style = self.get_selection(["Dirk", "Derek"])
        self.log_and_print("Selected drive style:", drive_style)

        if drive_style == "Dirk":
            self.user_preferences = DirkPreferences
        elif drive_style == "Derek":
            self.user_preferences = DerekPreferences

        self.log_and_print("Set up user preferences:", drive_style)

        if self.user_preferences == DirkPreferences:
            self.setup_dirk_preferences()
        elif self.user_preferences == DerekPreferences:
            self.setup_derek_preferences()

    def driver_control_periodic(self):
        left_speed = right_speed = 0
        if self.user_preferences.CONTROLLER_BINDINGS_STYLE == ControlStyles.TANK:
            left_speed = self.controller.left_stick_y()
            right_speed = self.controller.right_stick_y()
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
            left_speed = self.controller.left_stick_y()
            right_speed = self.controller.right_stick_y()

        left_speed = MathUtil.apply_deadband(left_speed)
        right_speed = MathUtil.apply_deadband(right_speed)

        left_speed, right_speed = desaturate_wheel_speeds([left_speed, right_speed])

        left_speed = MathUtil.cubic_filter(left_speed, linearity=self.user_preferences.CUBIC_FILTER_LINEARITY)
        right_speed = MathUtil.cubic_filter(right_speed, linearity=self.user_preferences.CUBIC_FILTER_LINEARITY)

        self.log_and_print("Updating drivetrain voltages - Left:", left_speed, "Right:", right_speed)
        self.drivetrain.set_voltage(left_speed * self.user_preferences.MAX_MOTOR_VOLTAGE,
                                    right_speed * self.user_preferences.MAX_MOTOR_VOLTAGE)

        self.drivetrain.update_odometry()
        self.wall_stake_mechanism.tick()

        self.brain.screen.draw_image_from_file(
            "/deploy/movie/output_frame_" + self.zpad_left(self.animation_frame, 6) + ".png", 0, 0)
        self.animation_frame += 1

    def setup_dirk_preferences(self):
        """Setup controller buttons for DirkPreferences."""
        self.controller.buttonB.pressed(self.mobile_goal_clamp.toggle_clamp)
        self.controller.buttonY.pressed(self.corner_mechanism.toggle_corner_mechanism)
        self.controller.buttonR1.pressed(self.wall_stake_mechanism.move_in)
        self.controller.buttonR1.pressed(
            lambda: self.log_and_print("Wall stake mechanism moving in") or self.wall_stake_mechanism.move_in)
        self.controller.buttonR1.released(
            lambda: self.log_and_print("Wall stake mechanism stopped") or self.wall_stake_mechanism.stop)
        self.controller.buttonL1.released(self.wall_stake_mechanism.stop)
        self.controller.buttonL2.pressed(self.scoring_mechanism.outtake)
        self.controller.buttonL2.released(self.scoring_mechanism.stop_motor)
        self.controller.buttonR2.pressed(self.scoring_mechanism.intake)
        self.controller.buttonR2.released(self.scoring_mechanism.stop_motor)
        self.controller.buttonDown.pressed(self.wall_stake_mechanism.dock)
        self.controller.buttonRight.pressed(self.wall_stake_mechanism.score)

    def setup_derek_preferences(self):
        """Setup controller buttons for DerekPreferences."""
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
