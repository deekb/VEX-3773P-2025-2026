import json

import AutonomousRoutines
import VEXLib.Math.MathUtil as MathUtil
from Constants import Preferences, CONTROL_STYLE_DIRK, CONTROL_STYLE_DEREK
from CornerMechanism import CornerMechanism
from Drivetrain import Drivetrain
from MobileGoalClamp import MobileGoalClamp
from ScoringMechanism import ScoringMechanism
from VEXLib.Robot.TimedRobot import TimedRobot
import VEXLib.Sensors.Controller
from VEXLib.Util import time
from VEXLib.Util.Logging import Logger
from WallStakeMechanism import WallStakeMechanism
from vex import *


class DirkPreferences(Preferences):
    CONTROLLER_BINDINGS_STYLE = CONTROL_STYLE_DEREK
    ARCADE_CONTROL = True


class DerekPreferences(Preferences):
    CONTROLLER_BINDINGS_STYLE = CONTROL_STYLE_DEREK
    ARCADE_CONTROL = True


class ScrollBufferedScreen:
    def __init__(self, max_lines=12):
        """
        Initialize the ScrollBufferedScreen with a specified maximum number of lines.

        :param max_lines: The maximum number of lines to keep in the buffer (default is 12).
        """
        self.max_lines = max_lines
        self.buffer = []

    def add_line(self, line):
        """
        Add a new line of text to the screen. Oldest lines are discarded once the limit is reached.

        :param line: The new line to add (string).
        """
        self.buffer.append(line)
        # Keep only the most recent `max_lines` lines
        if len(self.buffer) > self.max_lines:
            self.buffer.pop(0)

    def get_screen_content(self):
        """
        Retrieve the current screen content as a list of lines.

        :return: A list of strings representing the current content of the screen buffer.
        """
        return self.buffer

    def clear_screen(self):
        """
        Clear all lines from the screen buffer.
        """
        self.buffer = []


class Robot(TimedRobot):
    def __init__(self, brain):
        super().__init__(brain)
        self.controller = VEXLib.Sensors.Controller.Controller(PRIMARY)
        self.drivetrain = Drivetrain(
            [Motor(Constants.SmartPorts.FRONT_LEFT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, True),
             Motor(Constants.SmartPorts.MIDDLE_LEFT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, True),
             Motor(Constants.SmartPorts.REAR_LEFT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, True)],

            [Motor(Constants.SmartPorts.FRONT_RIGHT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, False),
             Motor(Constants.SmartPorts.MIDDLE_RIGHT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, False),
             Motor(Constants.SmartPorts.REAR_RIGHT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, False)],
        )

        self.screen = ScrollBufferedScreen()
        self.main_log = Logger(self.brain.sdcard, "main")
        self.print_log = Logger(self.brain.sdcard, "print")
        self.odometry_log = Logger(self.brain.sdcard, "odometry")
        self.competition_state_log = Logger(self.brain.sdcard, "competition_state")

        for log in [self.main_log, self.print_log, self.odometry_log, self.competition_state_log]:
            log.log("Robot Starting Up")

        self.mobile_goal_clamp = MobileGoalClamp()
        self.scoring_mechanism = ScoringMechanism()
        self.wall_stake_mechanism = WallStakeMechanism()
        self.doinker = CornerMechanism()
        self.animation_frame = 1
        self.autonomous_mappings = {
            "negative_4_rings_and_touch": AutonomousRoutines.negative_4_rings_and_touch,
            "negative": AutonomousRoutines.negative,
            "square_test": AutonomousRoutines.test_autonomous,
            "positive": AutonomousRoutines.positive,
            "win_point": AutonomousRoutines.win_point,
            "forwards": AutonomousRoutines.drive_forwards,
            "positive_WP": AutonomousRoutines.positive_win_point,
            "positive_2_mobile_goal": AutonomousRoutines.positive_2_mobile_goal,
        }

        self.autonomous = lambda *args: None

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
        self.log_and_print("Executing Autonomous Routine:", str(self.autonomous))
        self.autonomous(self)

    def on_enable(self):
        self.drivetrain.left_drivetrain_PID.reset()
        self.drivetrain.right_drivetrain_PID.reset()
        self.drivetrain.set_speed_percent(0, 0)
        self.drivetrain.update_motor_voltages()

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
            time.sleep_ms(5)

        return options[selection_index]

    def select_autonomous_routine(self):
        color = self.get_selection(["red", "blue", "skills", "skills_alliance_stake"])

        if "skills" in color:
            self.drivetrain.set_angles_inverted(False)
            if color == "skills":
                self.autonomous = AutonomousRoutines.skills
            elif color == "skills_alliance_stake":
                self.autonomous = AutonomousRoutines.skills_alliance_stake
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
        while self.drivetrain.inertial.is_calibrating():
            time.sleep_ms(5)

        self.wall_stake_mechanism.calibrate()
        self.controller.rumble("..")

        autonomous_routine = self.select_autonomous_routine()
        f = open("logs/autonomous_selection.log", "a")
        f.write(autonomous_routine + "\n")
        f.close()

        drive_style = self.get_selection(["Dirk", "Derek"])
        if drive_style == "Dirk":
            Preferences.ARCADE_CONTROL = False
            Preferences.CONTROLLER_BINDINGS_STYLE = CONTROL_STYLE_DIRK
        else:
            Preferences.ARCADE_CONTROL = True
            Preferences.CONTROLLER_BINDINGS_STYLE = CONTROL_STYLE_DEREK

        if Preferences.CONTROLLER_BINDINGS_STYLE == CONTROL_STYLE_DIRK:
            self.controller.buttonB.pressed(self.mobile_goal_clamp.toggle_clamp)
            self.controller.buttonY.pressed(self.doinker.toggle_corner_mechanism)

            self.controller.buttonR1.pressed(self.wall_stake_mechanism.move_in)
            self.controller.buttonR1.released(self.wall_stake_mechanism.stop)

            self.controller.buttonL1.pressed(self.wall_stake_mechanism.move_out)
            self.controller.buttonL1.released(self.wall_stake_mechanism.stop)

            self.controller.buttonL2.pressed(self.scoring_mechanism.outtake)
            self.controller.buttonL2.released(self.scoring_mechanism.stop_motor)

            self.controller.buttonR2.pressed(self.scoring_mechanism.intake)
            self.controller.buttonR2.released(self.scoring_mechanism.stop_motor)

            self.controller.buttonDown.pressed(self.wall_stake_mechanism.dock)
            self.controller.buttonRight.pressed(self.wall_stake_mechanism.score)

        elif Preferences.CONTROLLER_BINDINGS_STYLE == CONTROL_STYLE_DEREK:

            self.controller.buttonB.pressed(self.mobile_goal_clamp.toggle_clamp)
            self.controller.buttonY.pressed(self.doinker.toggle_corner_mechanism)

            self.controller.buttonL1.pressed(self.scoring_mechanism.intake)
            self.controller.buttonL1.released(self.scoring_mechanism.stop_motor)

            self.controller.buttonL2.pressed(self.scoring_mechanism.outtake)
            self.controller.buttonL2.released(self.scoring_mechanism.stop_motor)

            self.controller.buttonR2.pressed(self.wall_stake_mechanism.move_in)
            self.controller.buttonR2.released(self.wall_stake_mechanism.stop)

            self.controller.buttonR1.pressed(self.wall_stake_mechanism.move_out)
            self.controller.buttonR1.released(self.wall_stake_mechanism.stop)

            self.controller.buttonDown.pressed(self.wall_stake_mechanism.dock)
            self.controller.buttonRight.pressed(self.wall_stake_mechanism.score)

    def driver_control_periodic(self):
        if Preferences.ARCADE_CONTROL:
            forward_speed = self.controller.left_stick_y()
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

            # left_speed = MathUtil.cubic_filter(left_speed, linearity=0.4)
            # right_speed = MathUtil.cubic_filter(right_speed, linearity=0.4)

            self.drivetrain.set_voltage(left_speed * 10, right_speed * 10)

        self.odometry_log.log(self.drivetrain.odometry.get_pose())

        self.drivetrain.update_odometry()
        self.wall_stake_mechanism.tick()

        self.brain.screen.draw_image_from_file("/deploy/movie/output_frame_" + self.zpad_left(self.animation_frame, 6) + ".png", 0, 0)
        # self.brain.screen.draw_image_from_file("/deploy/logo_vertical_frame_" + str(self.animation_frame) + ".png", 0, 0)
        self.animation_frame += 1
        # if self.animation_frame > 10:
        #     self.animation_frame = 1
