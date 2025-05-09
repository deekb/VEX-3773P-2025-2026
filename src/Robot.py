import AutonomousRoutines
import VEXLib.Math.MathUtil as MathUtil
from Constants import *
from CornerMechanism import CornerMechanism
from Drivetrain import Drivetrain
from MobileGoalClamp import MobileGoalClamp
from RingRushMechanism import RingRushMechanism
from ScoringMechanism import ScoringMechanism
from VEXLib.Kinematics import desaturate_wheel_speeds
from VEXLib.Motor import Motor
from VEXLib.Robot.RobotBase import RobotBase
from VEXLib.Robot.ScrollingScreen import ScrollingScreen
from VEXLib.Sensors.Controller import DoublePressHandler, Controller
from VEXLib.Util import time, pass_function
from VEXLib.Util.Buffer import Buffer
from WallStakeMechanism import WallStakeMechanism, WallStakeState
from vex import Competition, PRIMARY, Rotation, Optical, Distance, DigitalOut, DEGREES, Color, FontType, \
    Inertial, Thread

# main_log = Logger(Brain().sdcard, Brain().screen, "robot")


class Robot(RobotBase):
    def __init__(self, brain):
        super().__init__(brain)
        # self.serial_communication = SerialCommunication("/dev/port6", "/dev/port7")

        self.brain.screen.set_font(FontType.MONO12)

        self.controller = Controller(PRIMARY)
        self.drivetrain = Drivetrain(
            [Motor(SmartPorts.FRONT_LEFT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, True),
             Motor(SmartPorts.REAR_LOWER_LEFT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, True),
             Motor(SmartPorts.REAR_UPPER_LEFT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, False)],
            [Motor(SmartPorts.FRONT_RIGHT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, False),
             Motor(SmartPorts.REAR_LOWER_RIGHT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, False),
             Motor(SmartPorts.REAR_UPPER_RIGHT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, True)],
            Inertial(SmartPorts.INERTIAL_SENSOR),
            self.log_and_print)

        self.screen = ScrollingScreen(self.brain.screen, Buffer(20))
        # self.main_log = main_log
        self.alliance_color = None

        self.mobile_goal_clamp = MobileGoalClamp(ThreeWirePorts.MOBILE_GOAL_CLAMP_PISTON)
        self.ring_rush_mechanism = RingRushMechanism(ThreeWirePorts.RING_RUSH_MECHANISM_PISTON)
        self.corner_mechanism = CornerMechanism(DigitalOut(ThreeWirePorts.LEFT_DOINKER_PISTON), DigitalOut(ThreeWirePorts.RIGHT_DOINKER_PISTON))

        self.scoring_mechanism = ScoringMechanism(
            Motor(Ports.PORT1, GearSetting.RATIO_18_1, False),
            Motor(Ports.PORT7, GearSetting.RATIO_18_1, True),
            Rotation(Ports.PORT18),
            Optical(Ports.PORT4),
            Distance(Ports.PORT10),
            self.brain.screen)

        self.wall_stake_mechanism = WallStakeMechanism(
            Motor(Ports.PORT8, GearSetting.RATIO_18_1, False),
            Rotation(Ports.PORT21))

        self.double_press_handler = DoublePressHandler(
            self.wall_stake_mechanism.previous_state,
            lambda: self.wall_stake_mechanism.transition_to(WallStakeState.DOCKED))

        self.user_preferences = DefaultPreferences
        # TODO: This string slice is jank as hell, it's literally slicing the name from this: "<function some_function at 0x7b8b993a>" I should make auto class-based or something and implement a get_name or better yet __str__/__repr__ function
        self.autonomous_mappings = {str(function)[10:-14]: function for function in AutonomousRoutines.available_autos}
        self.autonomous = pass_function
        self.competition = Competition(self.on_driver_control, self.on_autonomous)
        self.color_sort_tick_thread = None
        
        self.setup_complete = False

    def log_and_print(self, *parts):
        self.brain.screen.set_font(FontType.MONO15)
        message = " ".join(map(str, parts))
        self.screen.print(message)
        # self.main_log.log(message)
        print(message)

    def on_autonomous(self):
        # while not self.setup_complete:
        #     time.sleep_ms(20)
        # if self.alliance_color == "red":
        #     self.main_log.debug("Alliance color is", self.alliance_color)
        #     self.main_log.debug("Using left side corner mechanism")
        #     self.corner_mechanism.active_side = Sides.LEFT
        # elif self.alliance_color == "blue":
        #     self.main_log.debug("Alliance color is", self.alliance_color)
        #     self.main_log.debug("Using right side corner mechanism")
        #     self.corner_mechanism.active_side = Sides.RIGHT

        # self.main_log.debug("Executing chosen autonomous routine:", str(self.autonomous))
        # self.main_log.debug("Starting color_sort_tick_thread")
        # self.scoring_mechanism.log.info("Starting color_sort_tick_thread")
        self.color_sort_tick_thread = Thread(self.scoring_mechanism.loop, (self.alliance_color,))
        # self.main_log.debug("Started color_sort_tick_thread")
        # self.scoring_mechanism.log.info("Started color_sort_tick_thread")
        self.autonomous(self)

    def select_autonomous_routine(self):
        # self.main_log.debug("Starting autonomous routine selection")
        # self.main_log.trace("Available autonomous routines:", self.autonomous_mappings)
        autonomous_type = self.controller.get_selection(["red", "blue", "skills_alliance_stake"])
        # self.main_log.debug("Autonomous type:", autonomous_type)
        self.alliance_color = {"red": "red", "blue": "blue", "skills_alliance_stake": "red"}[autonomous_type]
        
        if "skills" in autonomous_type:
            self.drivetrain.set_angles_inverted(False)
            # self.main_log.trace("set_angles_inverted: False")
            self.autonomous = AutonomousRoutines.skills
            # self.main_log.debug("Skills routine chosen:", autonomous_type)
            return autonomous_type

        auto = self.controller.get_selection(sorted(list(self.autonomous_mappings.keys())))
        angles_inverted = autonomous_type == "blue"
        self.drivetrain.set_angles_inverted(angles_inverted)
        # self.main_log.trace("set_angles_inverted:", angles_inverted)
        self.autonomous = self.autonomous_mappings[auto]
        # self.main_log.trace("Selected autonomous routine:", angles_inverted)
        return autonomous_type + " " + auto

    def start(self):
        # try:
        self.on_setup()
        # except Exception as e:
        #     exception_buffer = io.StringIO()
        #     sys.print_exception(e, exception_buffer)
        #     self.serial_communication.send(str(exception_buffer.getvalue()))
        #
        #     for log_entry in exception_buffer.getvalue().split("\n"):
        #         main_log.fatal(str(log_entry))
        #     raise e

    # @main_log.logged
    def on_setup(self):
        # Break down the setup process into dedicated steps.
        self.calibrate_sensors()
        self.align_robot(exit_condition=self.controller.buttonA.pressing)
        self.select_autonomous_and_drive_style()
        # self.main_log.info("Setup complete")
        # self.main_log.debug("Unlocking setup lock")
        self.setup_complete = True

    def calibrate_sensors(self):
        # self.main_log.info("Calibrating sensors")
        # Set initial sensor positions and calibrate mechanisms.
        self.wall_stake_mechanism.rotation_sensor.set_position(
            WallStakeMechanismProperties.DOCKED_POSITION.to_degrees(), DEGREES)

        # self.main_log.debug("Calibrating scoring mechanism")
        self.scoring_mechanism.calibrate()
        # self.main_log.debug("Calibrated scoring mechanism successfully")
        # self.main_log.debug("Calibrating inertial sensor")
        self.drivetrain.odometry.inertial_sensor.calibrate()
        while self.drivetrain.odometry.inertial_sensor.is_calibrating():
            time.sleep_ms(5)
        # self.main_log.debug("Calibrated inertial sensor successfully")

    # @main_log.logged
    def align_robot(self, exit_condition):
        # self.main_log.info("Waiting for robot alignment")
        # Define target rotations using degrees.
        target_rotations = [
            Rotation2d.from_degrees(0),
            Rotation2d.from_degrees(7.6),
            Rotation2d.from_degrees(-7.6),
            Rotation2d.from_degrees(39),
            Rotation2d.from_degrees(-39),
            Rotation2d.from_degrees(90),
            Rotation2d.from_degrees(-90),
            Rotation2d.from_degrees(130),
            Rotation2d.from_degrees(-130),
            Rotation2d.from_degrees(180),
        ]

        self.controller.rumble("..")
        self.log_and_print("Please line up robot...")
        self.log_and_print("The screen will turn green when properly aligned")

        while not exit_condition():
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
                self.brain.screen.print("Please Align")

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
        self.log_and_print("Selecting autonomous routine...")
        autonomous_routine = self.select_autonomous_routine()
        self.log_and_print("Selected autonomous routine:", autonomous_routine)

        drive_style = self.controller.get_selection(["Dirk", "Dirk No color sort", "Derek"])
        self.log_and_print("Selected drive style:", drive_style)

        if drive_style == "Dirk":
            self.user_preferences = DirkPreferences
            self.setup_dirk_preferences()
        elif drive_style == "Dirk No color sort":
            self.user_preferences = DirkPreferencesNoColorSort
            self.setup_dirk_preferences()
        elif drive_style == "Derek":
            self.user_preferences = DerekPreferences
            self.setup_derek_preferences()

        self.log_and_print("Set up user preferences:", drive_style)

        if self.user_preferences.MEASURE_DRIVETRAIN_PROPERTIES_ON_STARTUP:
            for message in self.drivetrain.measure_properties():
                self.log_and_print(message)

    def on_driver_control(self):
        self.ring_rush_mechanism.raise_ring_rush_mechanism()
        while not self.setup_complete and self.competition.is_driver_control():
            time.sleep_ms(20)
        if self.color_sort_tick_thread:
            self.color_sort_tick_thread.stop()
        while True:
            self.driver_control_periodic()
            time.sleep_ms(2)

    def driver_control_periodic(self):
        left_speed = right_speed = 0
        if self.user_preferences.CONTROL_STYLE == ControlStyles.TANK:
            left_speed = self.controller.left_stick_y()
            right_speed = self.controller.right_stick_y()
            left_speed = MathUtil.apply_deadband(left_speed)
            right_speed = MathUtil.apply_deadband(right_speed)
        elif self.user_preferences.CONTROL_STYLE in [ControlStyles.ARCADE, ControlStyles.SPLIT_ARCADE]:
            forward_speed = self.controller.left_stick_y()
            if self.user_preferences.CONTROL_STYLE == ControlStyles.ARCADE:
                target_turn_speed = self.controller.left_stick_x() * self.user_preferences.TURN_SPEED
                target_turn_speed = -MathUtil.apply_deadband(target_turn_speed)
            else:
                target_turn_speed = self.controller.right_stick_x() * self.user_preferences.TURN_SPEED
                target_turn_speed = -MathUtil.apply_deadband(target_turn_speed)
            if self.user_preferences.DO_TURN_DECAY:
                # scale speeds to -1 to 1
                self.drivetrain.update_drivetrain_velocities()
                speeds_scaled = list(
                    map(lambda speed: speed.to_meters_per_second() / DrivetrainProperties.MAX_ACHIEVABLE_SPEED.to_meters_per_second(), self.drivetrain.get_speeds()))
                current_turn = speeds_scaled[0] - speeds_scaled[1]
                turn_correction = (target_turn_speed - current_turn) * 1

                left_speed = forward_speed - turn_correction
                right_speed = forward_speed + turn_correction
            else:
                left_speed = forward_speed - target_turn_speed
                right_speed = forward_speed + target_turn_speed
            forward_speed = MathUtil.apply_deadband(forward_speed)

        else:
            self.log_and_print("Invalid controller bindings style:", self.user_preferences.CONTROL_STYLE)

        left_speed, right_speed = desaturate_wheel_speeds([left_speed, right_speed])
        left_speed = MathUtil.clamp(left_speed, -1, 1)
        right_speed = MathUtil.clamp(right_speed, -1, 1)
        left_speed = MathUtil.cubic_filter(left_speed, linearity=self.user_preferences.CUBIC_FILTER_LINEARITY)
        right_speed = MathUtil.cubic_filter(right_speed, linearity=self.user_preferences.CUBIC_FILTER_LINEARITY)

        speeds = self.drivetrain.get_speeds()

        if self.user_preferences.ENABLE_DRIVING:
            if self.user_preferences.USE_PIDF_CONTROL:
                self.drivetrain.set_speed_zero_to_one(left_speed, right_speed)
                self.drivetrain.update_powers()
            else:
                self.drivetrain.set_powers(left_speed * self.user_preferences.MOVE_SPEED,
                                           right_speed * self.user_preferences.MOVE_SPEED)

        self.drivetrain.update_odometry()

        if self.user_preferences.COLOR_SORT and (not self.controller.buttonDown.pressing()):
            self.scoring_mechanism.tick(self.alliance_color)

    def setup_dirk_preferences(self):
        self.log_and_print("Setting up Dirk Preferences")
        self.controller.buttonB.pressed(
            lambda: [self.log_and_print("Toggling clamp"), self.mobile_goal_clamp.toggle_clamp()])

        self.controller.buttonL2.pressed(lambda: [self.log_and_print("Outtake"), self.scoring_mechanism.outtake()])
        self.controller.buttonL2.released(self.scoring_mechanism.stop_motor)
        self.controller.buttonR2.pressed(lambda: [self.log_and_print("Intake"), self.scoring_mechanism.intake()])
        self.controller.buttonR1.pressed(self.wall_stake_mechanism.next_state)
        self.controller.buttonL1.pressed(self.double_press_handler.press)
        self.controller.buttonR2.released(
            lambda: self.scoring_mechanism.set_speed(-35) or time.sleep(0.05) or self.scoring_mechanism.stop_motor())
        
        self.controller.buttonRight.pressed(self.corner_mechanism.toggle_left_corner_mechanism)
        self.controller.buttonY.pressed(self.corner_mechanism.toggle_right_corner_mechanism)

    def setup_derek_preferences(self):
        self.log_and_print("Setting up Derek Preferences")
        self.controller.buttonUp.pressed(lambda: self.drivetrain.turn_to(Rotation2d.from_degrees(0)))
        self.controller.buttonLeft.pressed(lambda: self.drivetrain.turn_to(Rotation2d.from_degrees(90)))
        self.controller.buttonDown.pressed(lambda: self.drivetrain.turn_to(Rotation2d.from_degrees(180)))
        self.controller.buttonRight.pressed(lambda: self.drivetrain.turn_to(Rotation2d.from_degrees(270)))
        self.controller.buttonB.pressed(self.mobile_goal_clamp.toggle_clamp)
        self.controller.buttonL1.pressed(self.scoring_mechanism.intake)
        self.controller.buttonX.pressed(self.ring_rush_mechanism.lower_ring_rush_mechanism)
        self.controller.buttonX.released(self.ring_rush_mechanism.raise_ring_rush_mechanism)
        self.controller.buttonL1.released(self.scoring_mechanism.stop_motor)
        self.controller.buttonL2.pressed(self.scoring_mechanism.outtake)
        self.controller.buttonL2.released(self.scoring_mechanism.back_off)
        self.controller.buttonR1.pressed(self.wall_stake_mechanism.next_state)
        self.controller.buttonR2.pressed(self.wall_stake_mechanism.previous_state)
        self.controller.buttonY.pressed(
            lambda: self.log_and_print("Toggling corner mechanism") or self.corner_mechanism.toggle_left_corner_mechanism())
