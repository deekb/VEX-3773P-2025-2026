import json
import sys

import AutonomousRoutines
import VEXLib.Math.MathUtil as MathUtil
from Constants import Preferences, CONTROL_STYLE_DIRK, CONTROL_STYLE_DEREK
from CornerMechanism import CornerMechanism
from Drivetrain import Drivetrain
from MobileGoalClamp import MobileGoalClamp
from ScoringMechanism import ScoringMechanism
from VEXLib.Robot.TimedRobot import TimedRobot
from VEXLib.Util import time
from WallStakeMechanism import WallStakeMechanism
from vex import *


class DirkPreferences(Preferences):
    CONTROLLER_BINDINGS_STYLE = CONTROL_STYLE_DEREK
    ARCADE_CONTROL = True


class DerekPreferences(Preferences):
    CONTROLLER_BINDINGS_STYLE = CONTROL_STYLE_DEREK
    ARCADE_CONTROL = True


class Logger:
    def __init__(self, sd_card, log_name_prefix):
        """
        Initializes the logger by creating or reading an 'index.json' file to manage log file numbering.
        Opens a single log file for writing during the program lifecycle.

        :param log_name_prefix: Prefix for the log file names.
        """
        self.sd_card = sd_card
        self.log_name_prefix = log_name_prefix
        self.index_file = "logs/index.json"
        self.current_index = self._get_current_index()
        self.log_file_path = "logs/" + str(self.log_name_prefix) + "-" + str(self.current_index) + ".log"
        self.log_file = None

        # Increment the index for the next usage and save it back to the 'index.json'
        self._increment_index()

        # Open the log file once for the entire program run
        self._open_log_file()

    def _get_current_index(self):
        """
        Retrieves the current logging index from 'index.json'. If the file doesn't exist, it initializes the index at 1.
        :return: Current index for the log file.
        """
        print()

        if self.sd_card.filesize(self.index_file):
            with open(self.index_file, "r") as file:
                try:
                    data = json.load(file)
                    return data.get("index", 1)
                except json.JSONDecodeError:
                    # Handle case where JSON file is corrupted
                    return 1
        else:
            return 1

    def _increment_index(self):
        """
        Increments the log file index and saves it back to 'index.json'.
        """
        with open(self.index_file, "w") as file:
            json.dump({"index": self.current_index + 1}, file)

    def _open_log_file(self):
        """
        Opens the log file in append mode for writing.
        """
        self.log_file = open(self.log_file_path, "a")

    def log(self, message):
        """
        Logs a message to the log file. Writes the message into the open file.

        :param message: Message to be logged.
        """
        self.log_file.write(message + "\n")
        self.log_file.flush()  # Ensure logs are written to the file immediately

    def close(self):
        """
        Closes the log file when the logger is no longer needed.
        """
        if self.log_file:
            self.log_file.close()

    def __del__(self):
        """
        Ensures the log file is closed automatically when the logger is deleted.
        """
        self.close()


logger = Logger(Brain().sdcard, "autonomous")
logger.log("This is autonomous")
logger.log("Testing")
logger.log("hello...")
logger.close()
print("Logging test done")


class Robot(TimedRobot):
    def __init__(self, brain):
        super().__init__(brain)
        self.controller = Controller(PRIMARY)
        self.drivetrain = Drivetrain()
        self.mobile_goal_clamp = MobileGoalClamp()
        self.scoring_mechanism = ScoringMechanism()
        self.wall_stake_mechanism = WallStakeMechanism()
        self.doinker = CornerMechanism()
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
        # self.animation_thread = Thread(self.animation)

    def animation(self):
        i = 1

        while True:
            self.brain.screen.draw_image_from_file("/deploy/logo_vertical_frame_" + str(i) + ".png", 0, 0)
            time.sleep_ms(10)
            i += 1
            if i > 10:
                i = 1

    def debug_wait(self):
        while not self.controller.buttonA.pressing():
            pass
        while self.controller.buttonA.pressing():
            pass

    def on_autonomous(self):
        self.brain.screen.print("Autonomous: ")
        self.brain.screen.print(self.autonomous)
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

    def on_setup(self):
        self.drivetrain.inertial.calibrate()
        while self.drivetrain.inertial.is_calibrating():
            time.sleep_ms(5)

        self.wall_stake_mechanism.calibrate()
        self.controller.rumble("....")

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
            forward_speed = self.controller.axis3.position() / 100
            turn_speed = self.controller.axis1.position() / 100

            forward_speed = MathUtil.apply_deadband(forward_speed, 0.05, 1)
            turn_speed = -MathUtil.apply_deadband(turn_speed, 0.05, 1)

            left_speed = forward_speed - turn_speed
            right_speed = forward_speed + turn_speed
        else:
            left_speed = self.controller.axis3.position() / 100
            right_speed = self.controller.axis2.position() / 100

            left_speed = MathUtil.apply_deadband(left_speed, 0.05, 1)
            right_speed = MathUtil.apply_deadband(right_speed, 0.05, 1)

        if Preferences.VOLTAGE_CONTROL:

            # left_speed = MathUtil.cubic_filter(left_speed, linearity=0.4)
            # right_speed = MathUtil.cubic_filter(right_speed, linearity=0.4)

            self.drivetrain.set_voltage(left_speed * 10, right_speed * 10)
        else:
            self.drivetrain.update_motor_voltages()

        if Preferences.PRINT_POSE:
            print(self.drivetrain.odometry.get_pose())

        self.drivetrain.update_odometry()
        self.wall_stake_mechanism.tick()
