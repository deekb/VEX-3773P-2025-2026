from VEXLib.Algorithms.PID import PIDController
from VEXLib.Algorithms.PIDF import PIDFController
from VEXLib.Geometry.Translation2d import Translation2d
from shelve import Shelf
from Logging import Logger

# This gets done first so any loggers that are created during imports use the updated index
startup_count = Shelf("logs/startup_count.csv")
startup_count.set("startup_count", startup_count.get("startup_count", -1) + 1)
robot_log = Logger("logs/robot")

import io
import math
import sys

import VEXLib.Math.MathUtil as MathUtil
from JoystickCalibration import normalize_joystick_input
from MatchLoadHelper import MatchLoadHelper
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
from AutonomousRoutines import DoNothingAutonomous, all_routines, Skills
from VEXLib.Util.motor_analysis import collect_power_relationship_data
from vex import Competition, Color, FontType, Inertial, DigitalOut, DEGREES

SmartPorts = CompetitionSmartPorts


class Robot(RobotBase):
    def __init__(self, brain):
        robot_log.info("Robot __init__ called")

        super().__init__(brain)
        self.brain.screen.set_font(FontType.MONO12)

        self.controller = Controller()
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

        self.driver_rotation_pid = PIDController(PIDGains(3, 0, 0))

        self.match_load_helper = MatchLoadHelper(DigitalOut(ThreeWirePorts.SCORING_SOLENOID))

        self.intake = Intake(
            Motor(SmartPorts.UPPER_INTAKE_MOTOR, GearRatios.INTAKE, True),
            Motor(SmartPorts.FLOATING_INTAKE_MOTOR, GearRatios.INTAKE, False),
            Motor(SmartPorts.HOOD_MOTOR, GearRatios.HOOD, False),
            DigitalOut(ThreeWirePorts.SCORING_SOLENOID),
        )

        self.screen = ScrollingScreen(self.brain.screen, Buffer(20))
        self.alliance_color = None

        self.user_preferences = DefaultPreferences

        self.competition = Competition(self.on_driver_control, self.on_autonomous)

        self.available_autonomous_routines = all_routines
        self.selected_autonomous = DoNothingAutonomous(self)

        self.brain.screen.pressed(self.flush_all_logs)

        self.setup_complete = False

    def flush_all_logs(self, message="Screen pressed; flushing logs manually"):
        robot_log.info("Flushing all logs")
        for log in [robot_log, self.drivetrain.log]:
            log.info(message)
            log.flush_logs()

    def log_and_print(self, *parts):
        self.brain.screen.set_font(FontType.MONO15)
        message = " ".join(map(str, parts))
        self.screen.print(message)
        robot_log.log(message)
        print(message)

    def select_autonomous_routine(self):
        robot_log.debug("Starting autonomous routine selection")
        robot_log.trace("Available autonomous routines:", self.available_autonomous_routines)
        autonomous_type = self.controller.get_selection(
            ["red", "blue", "skills"]
        )
        robot_log.debug("Autonomous type:", autonomous_type)
        self.alliance_color = {
            "red": "red",
            "blue": "blue",
            "skills": "red",
        }[autonomous_type]

        if "skills" in autonomous_type:
            self.drivetrain.set_angles_inverted(False)
            robot_log.trace("set_angles_inverted: False")
            self.selected_autonomous = Skills(self)
            robot_log.debug("Skills routine chosen:", autonomous_type)
            return autonomous_type

        selected_auto = self.controller.get_selection([auto.name for auto in self.available_autonomous_routines])
        angles_inverted = autonomous_type == "blue"
        self.drivetrain.set_angles_inverted(angles_inverted)
        robot_log.trace("set_angles_inverted:", angles_inverted)

        for autonomous in self.available_autonomous_routines:
            if selected_auto == autonomous.name:
                self.selected_autonomous = autonomous(self)
                break

        if isinstance(self.selected_autonomous, DoNothingAutonomous):
            robot_log.warn("DoNothingAutonomous autonomous routine selected")

        return autonomous_type + " " + self.selected_autonomous.name

    def start(self):
        robot_log.info("Robot start called")
        try:
            self.on_setup()
        except Exception as e:
            exception_buffer = io.StringIO()
            sys.print_exception(e, exception_buffer)
            for log_entry in exception_buffer.getvalue().split("\n"):
                robot_log.fatal(str(log_entry))
            robot_log.flush_logs()
            raise e

    @robot_log.logged
    def on_setup(self):
        robot_log.info("Robot on_setup called")
        # Break down the setup process into dedicated steps.
        self.calibrate_sensors()
        self.select_autonomous_and_drive_style()
        self.align_robot()
        robot_log.info("Setup complete")
        robot_log.debug("Unlocking setup lock")

        # time.sleep(2)
        #
        # if self.controller.buttonA.pressing():
        #     with open("logs/left_drivetrain.csv", "w") as f:
        #         f.flush()
        #         f.close()
        #     with open("logs/right_drivetrain.csv", "w") as f:
        #         f.flush()
        #         f.close()
        #
        #     collect_power_relationship_data("logs/left_drivetrain.csv", self.drivetrain.left_motors)
        #     time.sleep(3)
        #     collect_power_relationship_data("logs/right_drivetrain.csv", self.drivetrain.right_motors)

        self.setup_complete = True

    @robot_log.logged
    def calibrate_sensors(self):
        robot_log.info("Calibrating sensors")
        # Set initial sensor positions and calibrate mechanisms.

        robot_log.debug("Calibrating inertial sensor")
        self.drivetrain.odometry.inertial_sensor.calibrate()
        while self.drivetrain.odometry.inertial_sensor.is_calibrating():
            time.sleep_ms(5)
        robot_log.debug("Calibrated inertial sensor successfully")
        self.controller.rumble("..")

    @robot_log.logged
    def align_robot(self):
        robot_log.info("Aligning robot")
        robot_log.info("Waiting for robot alignment")
        target_rotation = self.selected_autonomous.startup_angle()
        self.controller.rumble("--")

        self.log_and_print("Please line up robot...")
        self.log_and_print("The screen will turn green when properly aligned")

        while not self.controller.buttonA.pressing():
            # Get the current rotation as a Rotation2d object.
            current_rotation = self.drivetrain.odometry.get_rotation()

            # Initialize variables for the minimum signed error.
            min_signed_error = None
            min_abs_error = float("inf")
            # Calculate the signed error for each target and find the minimum absolute error.
            error_rotation = (current_rotation - target_rotation).normalize()
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
        final_deg = self.drivetrain.odometry.get_rotation_normalized().to_degrees()
        self.brain.screen.clear_screen()
        self.log_and_print("Lined up, current angle:", final_deg)

    def select_autonomous_and_drive_style(self):
        robot_log.info("Selecting autonomous and drive style")
        autonomous_routine = self.select_autonomous_routine()
        self.log_and_print("Selected autonomous routine:", autonomous_routine)
        self.selected_autonomous.pre_match_setup()

        drive_style = self.controller.get_selection(
            ["Colton",
             "Debug"]
        )
        self.log_and_print("Selected drive style:", drive_style)

        if drive_style == "Colton":
            self.user_preferences = ColtonPreferences
            self.setup_default_bindings()
        elif drive_style == "Debug":
            self.user_preferences = DebugPreferences
            self.setup_default_bindings()

        self.log_and_print("Set up user preferences:", drive_style)

    @robot_log.logged
    def on_driver_control(self):
        self.flush_all_logs("Flushing logs before driver control")
        self.drivetrain.left_drivetrain_PID.pid_gains = self.user_preferences.PIDF_GAINS
        self.drivetrain.right_drivetrain_PID.pid_gains = self.user_preferences.PIDF_GAINS
        robot_log.trace("Driver control started")
        self.intake.stop_intake()
        self.intake.stop_hood()
        self.intake.raise_intake()
        while not self.setup_complete and self.competition.is_driver_control():
            time.sleep_ms(20)
        self.brain.screen.clear_screen()
        while True:
            self.driver_control_periodic()
            time.sleep_ms(2)

    @robot_log.logged
    def on_autonomous(self):
        self.drivetrain.left_drivetrain_PID.pid_gains = PIDFGains(0.25, 0.1, 0, 0.6)
        self.drivetrain.right_drivetrain_PID.pid_gains = PIDFGains(0.25, 0.1, 0, 0.6)
        self.drivetrain.odometry.pose.translation = Translation2d()
        self.drivetrain.target_pose = self.drivetrain.odometry.pose
        self.drivetrain.rotation_PID.setpoint = self.drivetrain.target_pose.rotation.to_radians()
        self.selected_autonomous.execute()

    def driver_control_periodic(self):
        left_speed, right_speed = self.controller.get_wheel_speeds(self.user_preferences.CONTROL_STYLE)

        # target_forward_speed = self.controller.left_stick_y_raw()
        # target_rotational_speed = -self.controller.right_stick_x_raw()
        #
        # actual_speeds = self.drivetrain.get_speeds()
        # left_measured_speed = actual_speeds[0].to_meters_per_second() / DrivetrainProperties.MAX_ACHIEVABLE_SPEED.to_meters_per_second()
        # right_measures_speed = actual_speeds[1].to_meters_per_second() / DrivetrainProperties.MAX_ACHIEVABLE_SPEED.to_meters_per_second()
        # measured_rotational_speed = (left_measured_speed - right_measures_speed) / 2
        #
        # self.driver_rotation_pid.setpoint = target_rotational_speed
        # rotational_output_power = self.driver_rotation_pid.update(measured_rotational_speed)
        #
        # left_speed = target_forward_speed + rotational_output_power
        # right_speed = target_forward_speed - rotational_output_power

        if self.user_preferences.ENABLE_DRIVING:
            # self.drivetrain.set_powers(
            #     -left_speed * self.user_preferences.MOVE_SPEED,
            #     -right_speed * self.user_preferences.MOVE_SPEED,
            # )
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
            angle = math.atan2(left_stick_y_processed, left_stick_x_processed)
            left_stick_x_processed = math.cos(angle)
            left_stick_y_processed = math.sin(angle)

        if self.user_preferences.INPUT_DEBUG_MODE:
            self.brain.screen.set_pen_color(Color.RED)
            self.brain.screen.draw_pixel(left_stick_x * 100 + 120, -left_stick_y * 100 + 120)
            self.brain.screen.set_pen_color(Color.GREEN)
            self.brain.screen.draw_pixel(left_stick_x_processed * 100 + 360, -left_stick_y_processed * 100 + 120)
            # robot_log.info("Wheel Speeds Linear: " + str(self.drivetrain.get_speeds()))

        # self.intake.flaps_are_stalled()
        # if self.controller.buttonL1.pressing():
        #     if self.intake.flaps_are_stalled():
        #         self.intake.run_upper_intake(-1)
        #     else:
        #         self.intake.run_intake(1)
        # else:
        #     self.intake.stop_intake()

        # if self.controller.buttonX.pressing():
        #     # self.drivetrain.measure_properties()
        #     robot_log.info("Lifting mass and testing properties...")
        #     # collect_power_relationship_data(
        #     #     "logs/FRONT_RIGHT_DRIVETRAIN.csv", [self.drivetrain.right_motors[0]]
        #     # )
        #     # collect_power_relationship_data(
        #     #     "logs/REAR_LOWER_RIGHT_DRIVETRAIN.csv", [self.drivetrain.right_motors[1]]
        #     # )
        #     # collect_power_relationship_data(
        #     #     "logs/REAR_UPPER_RIGHT_DRIVETRAIN.csv", [self.drivetrain.right_motors[2]]
        #     # )
        #
        #     testing_motor = self.drivetrain.right_motors[2]
        #
        #     initial_position = testing_motor.position(DEGREES)
        #     robot_log.debug("Initial position of mass is {}".format(initial_position))
        #     # for test in ["GREEN_100G", "GREEN_200G", "GREEN_300G", "GREEN_400G", "GREEN_500G", "GREEN_600G", "GREEN_700G", "GREEN_800G"]:
        #     # for test in ["GREEN_900G", "GREEN_1000G", "GREEN_1100G", "GREEN_1200G", "GREEN_1300G", "GREEN_1400G", "GREEN_1500G", "GREEN_1600G"]:
        #     # for test in ["GREEN_1700G", "GREEN_1800G", "GREEN_1900G", "GREEN_2000G", "GREEN_2100G", "GREEN_2200G", "GREEN_2300G", "GREEN_2400G"]:
        #
        # mass = 2500
        # while True:
        #     test = "GREEN_" + str(mass)
        #     self.brain.screen.clear_screen()
        #     self.brain.screen.set_cursor(1, 1)
        #     robot_log.debug("Testing \"{}\"...".format(test))
        #     self.brain.screen.print("Testing \"{}\"...".format(test))
        #     time.sleep(5)
        #     collect_power_relationship_data(
        #         "logs/friction_tests/" + test + ".csv",
        #         [testing_motor],
        #         power_range=(0.0, 1.0)
        #     )
        #     robot_log.debug("Done")
        #     self.brain.screen.print("Done")
        #     self.brain.screen.next_row()
        #     time.sleep(1)
        #     self.brain.screen.print("Returning to start position...")
        #     robot_log.debug("Returning to start position...")
        #     testing_motor.set_velocity(100, PERCENT)
        #     testing_motor.spin_to_position(initial_position, DEGREES)
        #     self.brain.screen.print("Done")
        #     robot_log.debug("Done")
        #     robot_log.debug("Reset position of mass is {}".format(testing_motor.position(DEGREES)))
        #     time.sleep(3)
        #     mass += 100

    @robot_log.logged
    def setup_default_bindings(self):
        robot_log.info("Setting up default controller bindings")
        # self.controller.buttonL1.pressed(lambda: (self.intake.run_intake(-1.0), self.intake.run_floating_intake(-1.0), self.intake.run_hood(-1.0)))
        # self.controller.buttonL1.released(lambda: (self.intake.stop_intake(), self.intake.stop_hood(), self.intake.stop_floating_intake()))
        # self.controller.buttonL2.pressed(lambda: (self.intake.run_intake(1.0), self.intake.run_floating_intake(1.0), self.intake.run_hood(1.0)))
        # self.controller.buttonL2.released(lambda: (self.intake.stop_intake(), self.intake.stop_hood(), self.intake.stop_floating_intake()))

        self.controller.buttonL2.pressed(lambda: (self.intake.run_intake(-1.0), self.intake.run_hood(-1.0)))
        self.controller.buttonL2.released(lambda: (self.intake.stop_intake(),self.intake.stop_hood()))

        self.controller.buttonR1.pressed(
            lambda: (self.intake.run_upper_intake(1.0), self.intake.run_floating_intake(1.0), self.intake.stop_hood())
        )
        self.controller.buttonR1.released(
            lambda: (self.intake.stop_intake(), self.intake.stop_hood())
        )

        self.controller.buttonR2.pressed(
            lambda: (self.intake.run_upper_intake(-1.0), self.intake.run_floating_intake(-1.0), self.intake.stop_hood())
        )
        self.controller.buttonR2.released(
            lambda: (self.intake.stop_intake(), self.intake.stop_hood())
        )

        self.controller.buttonL1.pressed(lambda: self.intake.run_intake(1.0))
        self.controller.buttonL1.released(self.intake.stop_intake)
        self.controller.buttonX.pressed(self.intake.raise_intake)
        self.controller.buttonY.pressed(self.intake.lower_intake)
        #
        # self.controller.buttonY.pressed(lambda: (self.intake.run_hood(1.0)))
        # self.controller.buttonB.pressed(lambda: (self.intake.run_hood(-1.0)))
