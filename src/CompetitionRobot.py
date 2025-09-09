import io
import math
import sys
from math import atan2

import VEXLib.Math.MathUtil as MathUtil
from JoystickCalibration import normalize_joystick_input
from Constants import *
from VEXLib.Geometry.GeometryUtil import hypotenuse
from VEXLib.Subsystems.TankDrivetrain import Drivetrain
from VEXLib.Motor import Motor
from VEXLib.Robot.RobotBase import RobotBase
from VEXLib.Robot.ScrollingScreen import ScrollingScreen
from VEXLib.Sensors.Controller import Controller
from VEXLib.Util import time
from VEXLib.Util.Buffer import Buffer
from Intake import Intake
from Logging import Logger
from vex import (
    Competition,
    PRIMARY,
    Color,
    FontType,
    Inertial,
)


robot_log = Logger("logs/robot")

class Robot(RobotBase):
    def __init__(self, brain):
        robot_log.info("Robot __init__ called")
        super().__init__(brain)
        self.brain.screen.set_font(FontType.MONO12)

        self.controller = Controller(PRIMARY)
        self.drivetrain = Drivetrain(
            [
                Motor(
                    SmartPorts.FRONT_LEFT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, True
                ),
                Motor(
                    SmartPorts.REAR_LOWER_LEFT_DRIVETRAIN_MOTOR,
                    GearRatios.DRIVETRAIN,
                    True,
                ),
                Motor(
                    SmartPorts.REAR_UPPER_LEFT_DRIVETRAIN_MOTOR,
                    GearRatios.DRIVETRAIN,
                    False,
                ),
            ],
            [
                Motor(
                    SmartPorts.FRONT_RIGHT_DRIVETRAIN_MOTOR,
                    GearRatios.DRIVETRAIN,
                    False,
                ),
                Motor(
                    SmartPorts.REAR_LOWER_RIGHT_DRIVETRAIN_MOTOR,
                    GearRatios.DRIVETRAIN,
                    False,
                ),
                Motor(
                    SmartPorts.REAR_UPPER_RIGHT_DRIVETRAIN_MOTOR,
                    GearRatios.DRIVETRAIN,
                    True,
                ),
            ],
            Inertial(SmartPorts.INERTIAL_SENSOR),
            self.log_and_print,
        )

        self.intake = Intake(
            Motor(
                SmartPorts.LOWER_ROLLER_MOTOR,
                GearRatios.LOWER_ROLLER,
                False,
            ),
            Motor(
                SmartPorts.UPPER_ROLLER_MOTOR,
                GearRatios.UPPER_ROLLER,
                False,
            ),
            Motor(
                SmartPorts.BUCKET_ROLLER_MOTOR,
                GearRatios.BUCKET_ROLLER,
                False,
            )
        )

        self.screen = ScrollingScreen(self.brain.screen, Buffer(20))
        self.alliance_color = None

        self.user_preferences = DefaultPreferences

        self.competition = Competition(self.on_driver_control, self.on_autonomous)
        self.brain.screen.pressed(self.flush_all_logs)

        self.setup_complete = False
        self.debug_mode = False

    def flush_all_logs(self):
        robot_log.info("Flushing all logs")
        for log in [robot_log, self.drivetrain.log]:
            log.info("Screen pressed; flushing logs manually")
            log.flush_logs()

    def log_and_print(self, *parts):
        self.brain.screen.set_font(FontType.MONO15)
        message = " ".join(map(str, parts))
        self.screen.print(message)
        robot_log.log(message)
        print(message)

    # def select_autonomous_routine(self):
    #     self.main_log.debug("Starting autonomous routine selection")
    #     self.main_log.trace("Available autonomous routines:", self.autonomous_mappings)
    #     autonomous_type = self.controller.get_selection(
    #         ["red", "blue", "skills_alliance_stake"]
    #     )
    #     self.main_log.debug("Autonomous type:", autonomous_type)
    #     self.alliance_color = {
    #         "red": "red",
    #         "blue": "blue",
    #         "skills_alliance_stake": "red",
    #     }[autonomous_type]
    #
    #     if "skills" in autonomous_type:
    #         self.drivetrain.set_angles_inverted(False)
    #         self.main_log.trace("set_angles_inverted: False")
    #         self.autonomous = AutonomousRoutines.skills_alliance_stake
    #         self.main_log.debug("Skills routine chosen:", autonomous_type)
    #         return autonomous_type
    #
    #     auto = self.controller.get_selection(
    #         sorted(list(self.autonomous_mappings.keys()))
    #     )
    #     angles_inverted = autonomous_type == "blue"
    #     self.drivetrain.set_angles_inverted(angles_inverted)
    #     self.main_log.trace("set_angles_inverted:", angles_inverted)
    #     self.autonomous = self.autonomous_mappings[auto]
    #     self.main_log.trace("Selected autonomous routine:", angles_inverted)
    #     return autonomous_type + " " + auto

    def start(self):
        robot_log.info("Robot start called")
        try:
            self.on_setup()
        except Exception as e:
            exception_buffer = io.StringIO()
            sys.print_exception(e, exception_buffer)
            #     self.serial_communication.send(str(exception_buffer.getvalue()))
            #
            for log_entry in exception_buffer.getvalue().split("\n"):
                robot_log.fatal(str(log_entry))
            robot_log.flush_logs()
            raise e

    # @main_log.logged
    def on_setup(self):
        robot_log.info("Robot on_setup called")
        # Break down the setup process into dedicated steps.
        # self.calibrate_sensors()
        self.align_robot()
        self.select_autonomous_and_drive_style()

        time.sleep_ms(2000)
        if self.controller.buttonA.pressing():
            self.debug_mode = True
            self.controller.rumble("....")

        robot_log.info("Setup complete")
        robot_log.debug("Unlocking setup lock")
        self.setup_complete = True

    def calibrate_sensors(self):
        robot_log.info("Calibrating sensors")
        # Set initial sensor positions and calibrate mechanisms.

        # self.main_log.debug("Calibrating inertial sensor")
        # self.drivetrain.odometry.inertial_sensor.calibrate()
        # while self.drivetrain.odometry.inertial_sensor.is_calibrating():
        #     time.sleep_ms(5)
        # self.main_log.debug("Calibrated inertial sensor successfully")

    # @main_log.logged
    def align_robot(self):
        robot_log.info("Aligning robot")
        robot_log.info("Waiting for robot alignment")
        # Define target rotations using degrees.
        target_rotations = [
            Rotation2d.from_degrees(0),
            Rotation2d.from_degrees(90),
            Rotation2d.from_degrees(-90),
            Rotation2d.from_degrees(180),
        ]

        self.controller.rumble("..")
        self.log_and_print("Please line up robot...")
        self.log_and_print("The screen will turn green when properly aligned")

        while not self.controller.buttonA.pressing():
            # Get the current rotation as a Rotation2d object.
            current_rotation = self.drivetrain.odometry.get_rotation()

            # Initialize variables for the minimum signed error.
            min_signed_error = None
            min_abs_error = float("inf")
            # Calculate the signed error for each target and find the minimum absolute error.
            for target in target_rotations:
                error_rotation = (current_rotation - target).normalize()
                error_deg_signed = error_rotation.to_degrees()
                abs_error = abs(error_deg_signed)
                if abs_error < min_abs_error:
                    min_abs_error = abs_error
                    min_signed_error = error_deg_signed

            # Decide on the screen color based on the absolute error.
            if min_abs_error > 5.0:
                # More than 5° away: flash the screen.
                flash_period_ms = 500
                current_time = time.time_ms()  # Get current time in ms.
                if ((current_time // flash_period_ms) % 2) == 0:
                    screen_color = Color.RED
                    text_color = Color.BLACK
                else:
                    screen_color = Color.BLACK
                    text_color = Color.RED
            else:
                # Within 5°: interpolate hue from green (120° at 0° error) to red (0° at 5° error).
                ratio = min_abs_error / 5.0
                hue = MathUtil.interpolate(120, 0, ratio, allow_extrapolation=False)
                screen_color = Color().hsv(hue, 1, 1)
                text_color = Color.BLACK

            # Do all logic before drawing to the screen to prevent flashing
            # Determine direction based on the signed error.
            if min_signed_error >= 0:
                direction = "CW"
            else:
                direction = "CCW"

            # Display the absolute error (formatted to two decimals) and the direction.
            display_error = abs(min_signed_error)
            display_text = "{:.2f}° {}".format(display_error, direction)

            self.brain.screen.set_fill_color(screen_color)
            self.brain.screen.set_pen_color(screen_color)
            self.brain.screen.draw_rectangle(0, 0, 480, 240)

            self.brain.screen.set_font(FontType.MONO60)
            self.brain.screen.set_cursor(2, 4)
            self.brain.screen.set_pen_color(text_color)

            self.brain.screen.print(display_text)

            if min_abs_error < 0.25:
                self.brain.screen.set_cursor(3, 3)
                self.brain.screen.print("Lined Up :)")
            else:
                self.brain.screen.set_cursor(1, 2)
                self.brain.screen.print("Please Rotate")

            self.drivetrain.update_odometry()
            time.sleep_ms(20)

        # Reset colors
        self.brain.screen.set_fill_color(Color.BLACK)
        self.brain.screen.set_pen_color(Color.WHITE)

        # Final update and logging after button press.
        self.drivetrain.update_odometry()
        final_deg = self.drivetrain.odometry.get_rotation().to_degrees()
        self.brain.screen.clear_screen()
        self.log_and_print("Lined up, current angle:", final_deg)

    def select_autonomous_and_drive_style(self):
        robot_log.info("Selecting autonomous and drive style")
        # autonomous_routine = self.select_autonomous_routine()
        # self.log_and_print("Selected autonomous routine:", autonomous_routine)

        drive_style = self.controller.get_selection(
            ["Colton"]
        )
        self.log_and_print("Selected drive style:", drive_style)

        if drive_style == "Colton":
            self.user_preferences = ColtonPreferences
            self.setup_colton_preferences()

        self.log_and_print("Set up user preferences:", drive_style)

        # for message in self.drivetrain.measure_properties():
        #     self.log_and_print(message)

    def on_driver_control(self):
        robot_log.trace("Driver control started")
        while not self.setup_complete and self.competition.is_driver_control():
            time.sleep_ms(20)
        self.brain.screen.clear_screen()
        while True:
            self.driver_control_periodic()
            time.sleep_ms(2)

    def driver_control_periodic(self):
        robot_log.trace("Driver control periodic")

        left_speed, right_speed = self.controller.get_wheel_speeds(self.user_preferences.CONTROL_STYLE)

        if self.user_preferences.ENABLE_DRIVING:
            if self.user_preferences.USE_PIDF_CONTROL:
                self.drivetrain.set_speed_zero_to_one(left_speed, right_speed)
                self.drivetrain.update_powers()
            else:
                self.drivetrain.set_powers(
                    left_speed * self.user_preferences.MOVE_SPEED,
                    right_speed * self.user_preferences.MOVE_SPEED,
                )

        self.drivetrain.update_odometry()
        left_stick_x = self.controller.left_stick_x()
        left_stick_y = self.controller.left_stick_y()
        left_stick_x_processed, left_stick_y_processed = normalize_joystick_input(left_stick_x, left_stick_y)

        if hypotenuse(left_stick_x_processed, left_stick_y_processed) > 1:
            angle = atan2(left_stick_y_processed, left_stick_x_processed)
            left_stick_x_processed = math.cos(angle)
            left_stick_y_processed = math.sin(angle)

        if self.user_preferences.INPUT_DEBUG_MODE:
            self.brain.screen.set_pen_color(Color.RED)
            self.brain.screen.draw_pixel(left_stick_x * 100 + 120, -left_stick_y * 100 + 120)
            self.brain.screen.set_pen_color(Color.GREEN)
            self.brain.screen.draw_pixel(left_stick_x_processed * 100 + 360, -left_stick_y_processed * 100 + 120)

        if self.controller.buttonX.pressing():
            self.drivetrain.measure_properties()

    def setup_colton_preferences(self):
        robot_log.info("Setting up Colton preferences")
        self.controller.buttonL1.pressed(lambda: (self.intake.run_lower(-1.0), self.intake.run_bucket(1.0)))
        self.controller.buttonL1.released(lambda: (self.intake.stop_lower(), self.intake.stop_bucket()))
        self.controller.buttonL2.pressed(lambda: (self.intake.run_lower(1.0), self.intake.run_bucket(-1.0)))
        self.controller.buttonL2.released(lambda: (self.intake.stop_lower(), self.intake.stop_bucket()))

        self.controller.buttonR1.pressed(lambda: (self.intake.run_lower(-1.0), self.intake.run_bucket(-1.0), self.intake.run_upper(-1.0)))
        self.controller.buttonR1.released(lambda: (self.intake.stop_lower(), self.intake.stop_bucket(), self.intake.stop_upper()))
        self.controller.buttonR2.pressed(lambda: (self.intake.run_lower(-1.0), self.intake.run_bucket(-1.0), self.intake.run_upper(1.0)))
        self.controller.buttonR2.released(lambda: (self.intake.stop_lower(), self.intake.stop_bucket(), self.intake.stop_upper()))

        self.controller.buttonDown.pressed(lambda: self.intake.toggle_bucket_lock)
        self.controller.buttonY.pressed(self.drivetrain.verify_speed_pid)
