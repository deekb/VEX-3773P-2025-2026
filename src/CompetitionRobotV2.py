from VEXLib.Algorithms.PID import PIDController
from VEXLib.Geometry.Translation2d import Translation2d
from VEXLib.Util.Logging import TimeSeriesLogger
from shelve import Shelf
from Logging import Logger, NoLogger
from DescoringArm import DescoringArm
from ConstantsV2 import *


# This gets done first so any loggers that are created during imports use the updated index
startup_count = Shelf("logs/startup_count.csv")
startup_count.set("startup_count", startup_count.get("startup_count", -1) + 1)
if NO_LOGGING:
    robot_log = NoLogger("logs/robot")
    telemetry_log = NoLogger("logs/telemetry")
else:
    robot_log = Logger("logs/robot")
    telemetry_log = Logger("logs/telemetry")
# voltage_velocity = TimeSeriesLogger("logs/voltage_velocity.csv", ["time", "left_voltage", "right_voltage", "left_speed", "right_speed"])


import io
import math
import sys

import VEXLib.Math.MathUtil as MathUtil
from JoystickCalibration import normalize_joystick_input
from MatchLoadHelper import MatchLoadHelper
from VEXLib.Geometry.GeometryUtil import hypotenuse
from TankDrivetrainV2 import Drivetrain
from VEXLib.Motor import Motor
from VEXLib.Robot.RobotBase import RobotBase
from VEXLib.Robot.ScrollingScreen import ScrollingScreen
from VEXLib.Sensors.Controller import Controller
from VEXLib.Util import time
from VEXLib.Util.Buffer import Buffer
from IntakeV2 import IntakeV2
from AutonomousRoutinesV2 import DoNothingAutonomous, all_routines, Skills
from VEXLib.Util.motor_analysis import collect_power_relationship_data
from vex import (
    Competition,
    Color,
    FontType,
    Inertial,
    DigitalOut,
    DEGREES,
    TemperatureUnits,
    VoltageUnits,
    CurrentUnits,
    PERCENT, Optical,
)

SmartPorts = CompetitionSmartPorts


class Robot(RobotBase):
    def __init__(self, brain):
        robot_log.info("Robot __init__ called")

        super().__init__(brain)
        self.brain.screen.set_font(FontType.MONO12)

        self.controller = Controller()
        self.controller.add_deadband_step(0.05)
        # self.controller.add_cubic_step()

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

        self.calibrate_sensors()

        self.driver_rotation_pid = PIDController(PIDGains(3, 0, 0))

        self.intake = IntakeV2(
            Motor(SmartPorts.UPPER_INTAKE_MOTOR, GearRatios.UPPER_INTAKE, False),
            Motor(SmartPorts.FLOATING_INTAKE_MOTOR, GearRatios.UPPER_INTAKE, True),
            Motor(SmartPorts.HOOD_MOTOR, GearRatios.HOOD, False),
            DigitalOut(ThreeWirePorts.SCORING_SOLENOID),
            Optical(SmartPorts.COLOR_SENSOR)
        )

        self.match_load_helper = MatchLoadHelper(
            DigitalOut(ThreeWirePorts.MATCH_LOAD_HELPER_SOLENOID)
        )

        self.descoring_arm = DescoringArm(
            DigitalOut(ThreeWirePorts.DESCORING_ARM_SOLENOID)
        )

        self.screen = ScrollingScreen(self.brain.screen, Buffer(20))
        self.alliance_color = None

        self.user_preferences = DefaultPreferences

        self.competition = Competition(self.on_driver_control, self.on_autonomous)

        self.available_autonomous_routines = all_routines
        self.selected_autonomous = DoNothingAutonomous(self)

        self.brain.screen.pressed(self.flush_all_logs)

        self.setup_complete = False
        self.iteration_count = 0

    def flush_all_logs(self, message="Screen pressed; flushing logs manually"):
        robot_log.info("Flushing all logs")
        for log in [robot_log, self.drivetrain.log, self.drivetrain.debug_log]:
            log.info(message)
            log.flush_logs()

    def log_and_print(self, *parts):
        self.brain.screen.set_font(FontType.MONO15)
        message = " ".join(map(str, parts))
        self.screen.print(message)
        robot_log.log(message)
        print(message)

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
        robot_log.info("Selecting autonomous and drive style")
        robot_log.trace(
            "Available autonomous routines:", self.available_autonomous_routines
        )
        selected_auto, drive_style, alliance_color = self.controller.get_multiple_selections([[auto.name for auto in self.available_autonomous_routines], ["Colton", "Debug"], ["red", "blue"]])
        if alliance_color == "blue":
            self.alliance_color = Color.BLUE
        else:
            alliance_color = Color.RED

        for autonomous in self.available_autonomous_routines:
            if selected_auto == autonomous.name:
                self.selected_autonomous = autonomous(self)
                break

        if isinstance(self.selected_autonomous, DoNothingAutonomous):
            robot_log.warn("DoNothingAutonomous autonomous routine selected")

        self.log_and_print("Selected autonomous routine:", selected_auto)
        self.selected_autonomous.pre_match_setup()

        self.log_and_print("Selected drive style:", drive_style)

        if drive_style == "Colton":
            self.user_preferences = ColtonPreferences
            self.setup_default_bindings()
        elif drive_style == "Debug":
            self.user_preferences = DebugPreferences
            self.setup_debug_bindings()

        self.log_and_print("Set up user preferences:", drive_style)

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
        time.sleep(2)
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

    @robot_log.logged
    def on_driver_control(self):
        self.intake.stop_intake()
        self.selected_autonomous.cleanup()
        self.flush_all_logs("Flushing logs before driver control")
        self.drivetrain.left_drivetrain_PID.pid_gains = self.user_preferences.PIDF_GAINS_LEFT_DRIVER
        self.drivetrain.right_drivetrain_PID.pid_gains = self.user_preferences.PIDF_GAINS_RIGHT_DRIVER
        robot_log.trace("Driver control started")
        self.intake.stop_intake()
        self.intake.stop_hood()
        self.intake.raise_intake()
        while not self.setup_complete and self.competition.is_driver_control():
            time.sleep_ms(20)
        self.brain.screen.clear_screen()
        while True:
            self.driver_control_periodic()
            time.sleep_ms(10)

    @robot_log.logged
    def on_autonomous(self):
        self.intake.stop_intake()
        self.drivetrain.left_drivetrain_PID.pid_gains = self.user_preferences.PIDF_GAINS_LEFT_AUTO
        self.drivetrain.right_drivetrain_PID.pid_gains = self.user_preferences.PIDF_GAINS_RIGHT_AUTO
        self.drivetrain.odometry.pose.translation = Translation2d()
        self.drivetrain.target_pose = self.drivetrain.odometry.pose
        self.drivetrain.rotation_PID.setpoint = self.drivetrain.target_pose.rotation.to_radians()
        self.selected_autonomous.execute()

    def log_telemetry(self):
        self.iteration_count += 1
        if self.iteration_count % 100 == 0:
            telemetry_log.info("Telemetry at iteration", self.iteration_count)
            telemetry_log.info("Time: ", time.time())
            telemetry_log.info("Drivetrain Pose:", self.drivetrain.odometry.pose)
            telemetry_log.info("Left Motor temps:", [motor.temperature(TemperatureUnits.CELSIUS) for motor in self.drivetrain.left_motors])
            telemetry_log.info("Right Motor temps:", [motor.temperature(TemperatureUnits.CELSIUS) for motor in self.drivetrain.right_motors])
            telemetry_log.info("Battery Voltage:", self.brain.battery.voltage(VoltageUnits.VOLT))
            telemetry_log.info("Battery Temperature:", self.brain.battery.temperature(TemperatureUnits.CELSIUS))
            telemetry_log.info("Battery Current:", self.brain.battery.current(CurrentUnits.AMP))
            telemetry_log.info("Battery Capacity:", self.brain.battery.capacity())
            telemetry_log.flush_logs()

    def driver_control_periodic(self):
        self.log_telemetry()
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
                # self.drivetrain.get_speeds()
                # voltage_velocity.write_data({
                #     "time": time.time(),
                #     "left_voltage":left_speed,
                #     "right_voltage":right_speed,
                #     "left_speed": self.drivetrain.get_left_speed().to_meters_per_second(),
                #     "right_speed": self.drivetrain.get_right_speed().to_meters_per_second(),
                # })
                self.drivetrain.set_speed_zero_to_one(left_speed, right_speed)
                self.drivetrain.update_powers()
            else:
                # self.drivetrain.get_speeds()
                # voltage_velocity.write_data({
                #     "time": time.time(),
                #     "left_voltage":left_speed,
                #     "right_voltage":right_speed,
                #     "left_speed": self.drivetrain.get_left_speed().to_meters_per_second(),
                #     "right_speed": self.drivetrain.get_right_speed().to_meters_per_second(),
                # })
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

        self.ensure_match_loader_in_size()
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

    def ensure_match_loader_in_size(self):
        if (not self.intake.piston.value()) and self.match_load_helper.piston.value():
            self.match_load_helper.retract()
            robot_log.warn("Retracting match load helper because intake is down")
            self.controller.rumble("..")

    def toggle_intake(self):
        if self.intake.piston.value():
            self.descoring_arm.retract()
            self.intake.lower_intake()
        else:
            self.intake.raise_intake()

    @robot_log.logged
    def setup_default_bindings(self):
        robot_log.info("Setting up default controller bindings")

        self.controller.buttonL2.pressed(lambda: (self.intake.run_intake(-1.0), self.intake.run_hood(-1.0)))
        self.controller.buttonL2.released(lambda: (self.intake.stop_intake(),self.intake.stop_hood()))

        self.controller.buttonR1.pressed(
            lambda: (self.intake.run_intake(1.0), self.intake.stop_hood())
        )
        self.controller.buttonR1.released(
            lambda: (self.intake.stop_intake(), self.intake.stop_hood())
        )

        self.controller.buttonR2.pressed(
            lambda: (self.intake.run_intake(-1.0), self.intake.stop_hood())
        )
        self.controller.buttonR2.released(
            lambda: (self.intake.stop_intake(), self.intake.stop_hood())
        )

        self.controller.buttonL1.pressed(lambda: (self.intake.run_intake(1.0)))
        self.controller.buttonL1.released(self.intake.stop_intake)

        self.controller.buttonY.pressed(self.toggle_intake)

        self.controller.buttonB.pressed(self.match_load_helper.extend)
        self.controller.buttonB.released(self.match_load_helper.retract)

        self.controller.buttonDown.pressed(self.descoring_arm.toggle)

    @robot_log.logged
    def setup_debug_bindings(self):
        robot_log.info("Setting up debug controller bindings")
        self.setup_default_bindings()
        self.controller.buttonX.pressed(lambda: self.intake.intake_until_color_nonblocking(Color.RED, 1))
        self.controller.buttonA.pressed(lambda: self.intake.intake_until_color_nonblocking(Color.BLUE, 1))
