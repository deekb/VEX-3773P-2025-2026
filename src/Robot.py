from Constants import *
from vex import Competition, PRIMARY, Rotation, Optical, Distance, DigitalOut, DEGREES

import AutonomousRoutines
import VEXLib.Math.MathUtil as MathUtil
from CornerMechanism import CornerMechanism
from Drivetrain import Drivetrain
from MobileGoalClamp import MobileGoalClamp
from ScoringMechanism import ScoringMechanism
from VEXLib.Kinematics import desaturate_wheel_speeds
from VEXLib.Motor import Motor
from VEXLib.Robot.RobotBase import RobotBase
from VEXLib.Robot.ScrollBufferedScreen import ScrollBufferedScreen
from VEXLib.Sensors.Controller import DoublePressHandler, Controller
from VEXLib.Util import time, pass_function
from VEXLib.Util.Logging import Logger
from WallStakeMechanism import WallStakeMechanism, WallStakeState


class Robot(RobotBase):
    def __init__(self, brain):
        super().__init__(brain)
        self.controller = Controller(PRIMARY)
        self.drivetrain = Drivetrain([Motor(SmartPorts.FRONT_LEFT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, True),
                                      Motor(SmartPorts.REAR_LOWER_LEFT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, True),
                                      Motor(SmartPorts.REAR_UPPER_LEFT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, False)],

                                     [Motor(SmartPorts.FRONT_RIGHT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, False),
                                      Motor(SmartPorts.REAR_LOWER_RIGHT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, False),
                                      Motor(SmartPorts.REAR_UPPER_RIGHT_DRIVETRAIN_MOTOR, GearRatios.DRIVETRAIN, True)])

        self.screen = ScrollBufferedScreen()

        self.main_log = Logger(self.brain.sdcard, MAIN_LOG_FILENAME)

        self.alliance_color = None

        self.mobile_goal_clamp = MobileGoalClamp(ThreeWirePorts.MOBILE_GOAL_CLAMP_PISTON)

        self.corner_mechanism = CornerMechanism(DigitalOut(ThreeWirePorts.DOINKER_PISTON))

        self.scoring_mechanism = ScoringMechanism(Motor(Ports.PORT1, GearSetting.RATIO_18_1, False),
                                                  Motor(Ports.PORT4, GearSetting.RATIO_18_1, True),
                                                  Rotation(Ports.PORT18),
                                                  Optical(Ports.PORT10),
                                                  Distance(Ports.PORT5),
                                                  self.brain.screen)

        self.wall_stake_mechanism = WallStakeMechanism(Motor(Ports.PORT8, GearSetting.RATIO_18_1, False),
                                                       Rotation(Ports.PORT21))

        self.double_press_handler = DoublePressHandler(self.wall_stake_mechanism.previous_state,
                                                       lambda: self.wall_stake_mechanism.transition_to(WallStakeState.DOCKED))

        self.user_preferences = DefaultPreferences
        self.autonomous_mappings = {str(function)[10:]: function for function in AutonomousRoutines.available_autos}
        self.autonomous = pass_function
        self.competition = Competition(self.on_driver_control, self.on_autonomous)

    def log_and_print(self, *parts):
        message = " ".join(map(str, parts))
        self.screen.add_line(message)
        self.brain.screen.set_cursor(1, 1)
        self.brain.screen.clear_screen()
        for line in self.screen.get_screen_content():
            self.brain.screen.print(line)
            self.brain.screen.next_row()
        self.main_log.log(message)
        print(message)

    def on_autonomous(self):
        self.drivetrain.reset()
        self.log_and_print("Executing chosen autonomous routine:", str(self.autonomous))
        self.autonomous(self)

    def select_autonomous_routine(self):
        self.log_and_print("Starting autonomous routine selection")
        autonomous_type = self.controller.get_selection(["red", "blue", "skills_alliance_stake"])
        self.alliance_color = {"red": "red", "blue": "blue", "skills_alliance_stake": "red"}[autonomous_type]

        if autonomous_type == "skills_alliance_stake":
            self.drivetrain.set_angles_inverted(False)
            self.autonomous = AutonomousRoutines.skills_alliance_stake
            self.log_and_print("Skills routine chosen:", autonomous_type)
            return autonomous_type

        auto = self.controller.get_selection(sorted(list(self.autonomous_mappings.keys())))

        self.drivetrain.set_angles_inverted(autonomous_type == "blue")
        self.autonomous = self.autonomous_mappings[auto]

        return autonomous_type + " " + auto

    def start(self):
        self.on_setup()

    def on_setup(self):
        self.wall_stake_mechanism.rotation_sensor.set_position(-100, DEGREES)
        self.log_and_print("Calibrating inertial sensor...")
        self.drivetrain.odometry.inertial_sensor.calibrate()
        self.log_and_print("Calibrating scoring mechanism...")

        self.scoring_mechanism.calibrate()

        while self.drivetrain.odometry.inertial_sensor.is_calibrating():
            time.sleep_ms(5)
        self.log_and_print("Calibrated inertial sensor successfully")
        self.controller.rumble("..")
        self.log_and_print("Selecting autonomous routine...")
        autonomous_routine = self.select_autonomous_routine()
        self.log_and_print("Selected autonomous routine:", autonomous_routine)

        drive_style = self.controller.get_selection(["Dirk", "Derek"])
        self.log_and_print("Selected drive style:", drive_style)

        if drive_style == "Dirk":
            self.user_preferences = DirkPreferences
            self.setup_dirk_preferences()
        elif drive_style == "Derek":
            self.user_preferences = DerekPreferences
            self.setup_derek_preferences()

        self.log_and_print("Set up user preferences:", drive_style)

        if self.user_preferences.MEASURE_DRIVETRAIN_PROPERTIES_ON_STARTUP:
            for message in self.drivetrain.measure_properties():
                self.log_and_print(message)

        self.log_and_print("Setup complete")

    def on_driver_control(self):
        self.drivetrain.reset()
        while True:
            self.driver_control_periodic()
            time.sleep_ms(20)

    def driver_control_periodic(self):
        left_speed = right_speed = 0
        if self.user_preferences.CONTROL_STYLE == ControlStyles.TANK:
            left_speed = self.controller.left_stick_y()
            right_speed = self.controller.right_stick_y()

            left_speed = MathUtil.apply_deadband(left_speed)
            right_speed = MathUtil.apply_deadband(right_speed)
        elif self.user_preferences.CONTROL_STYLE in [ControlStyles.ARCADE, ControlStyles.SPLIT_ARCADE]:
            forward_speed = turn_speed = 0
            forward_speed = self.controller.left_stick_y()
            if self.user_preferences.CONTROL_STYLE == ControlStyles.ARCADE:
                turn_speed = self.controller.left_stick_x() * self.user_preferences.TURN_SPEED
            elif self.user_preferences.CONTROL_STYLE == ControlStyles.SPLIT_ARCADE:
                turn_speed = self.controller.right_stick_x() * self.user_preferences.TURN_SPEED

            forward_speed = MathUtil.apply_deadband(forward_speed)
            turn_speed = -MathUtil.apply_deadband(turn_speed)

            left_speed = forward_speed - turn_speed
            right_speed = forward_speed + turn_speed
        else:
            self.log_and_print("Invalid controller bindings style:", self.user_preferences.CONTROL_STYLE)

        left_speed, right_speed = desaturate_wheel_speeds([left_speed, right_speed])

        left_speed = MathUtil.clamp(left_speed, -1, 1)
        right_speed = MathUtil.clamp(right_speed, -1, 1)

        left_speed = MathUtil.cubic_filter(left_speed, linearity=self.user_preferences.CUBIC_FILTER_LINEARITY)
        right_speed = MathUtil.cubic_filter(right_speed, linearity=self.user_preferences.CUBIC_FILTER_LINEARITY)

        # if self.drivetrain.left_motors[0].velocity(PERCENT) > left_speed * 100:
        #     left_speed -= 0.1
        # if self.drivetrain.left_motors[0].velocity(PERCENT) < left_speed * 100:
        #     left_speed += 0.1
        #
        # if self.drivetrain.right_motors[0].velocity(PERCENT) < right_speed * 100:
        #     right_speed += 0.1
        # if self.drivetrain.right_motors[0].velocity(PERCENT) > right_speed * 100:
        #     right_speed -= 0.1

        # self.log_and_print("Updating drivetrain voltages - Left:", left_speed, "Right:", right_speed)
        self.drivetrain.set_powers(left_speed * self.user_preferences.MAX_MOTOR_VOLTAGE,
                                    right_speed * self.user_preferences.MAX_MOTOR_VOLTAGE)

        self.drivetrain.update_odometry()

        # if self.controller.buttonX.pressing():
        #     self.on_autonomous()
        self.scoring_mechanism.tick(self.alliance_color)

    def setup_dirk_preferences(self):
        """Setup controller buttons for DirkPreferences."""
        self.log_and_print("Setting up Dirk Preferences")
        self.controller.buttonB.pressed(
            lambda: self.log_and_print("Toggling clamp") or self.mobile_goal_clamp.toggle_clamp())
        self.controller.buttonL2.pressed(self.scoring_mechanism.outtake)
        self.controller.buttonL2.released(self.scoring_mechanism.stop_motor)
        self.controller.buttonR2.pressed(self.scoring_mechanism.intake)
        self.controller.buttonR1.pressed(self.wall_stake_mechanism.next_state)

        self.controller.buttonL1.pressed(self.double_press_handler.press)

        self.controller.buttonR2.released(
            lambda: self.scoring_mechanism.set_speed(-35) or time.sleep(0.05) or self.scoring_mechanism.stop_motor())

        self.controller.buttonY.pressed(self.corner_mechanism.toggle_corner_mechanism)
        self.controller.buttonRight.pressed(self.scoring_mechanism.intake_until_ring)

    def setup_derek_preferences(self):
        """Setup controller buttons for DerekPreferences."""
        self.log_and_print("Setting up Derek Preferences")
        self.controller.buttonUp.pressed(lambda: self.drivetrain.turn_to_gyro(0))
        self.controller.buttonLeft.pressed(lambda: self.drivetrain.turn_to_gyro(90))
        self.controller.buttonDown.pressed(lambda: self.drivetrain.turn_to_gyro(180))
        self.controller.buttonRight.pressed(lambda: self.drivetrain.turn_to_gyro(270))
        self.controller.buttonB.pressed(
            lambda: self.log_and_print("Toggling clamp") or self.mobile_goal_clamp.toggle_clamp())
        self.controller.buttonL1.pressed(self.scoring_mechanism.intake)
        self.controller.buttonL1.released(self.scoring_mechanism.stop_motor)
        self.controller.buttonL2.pressed(self.scoring_mechanism.outtake)
        self.controller.buttonL2.released(
            lambda: self.scoring_mechanism.set_speed(-35) or time.sleep(0.3) or self.scoring_mechanism.stop_motor())

        self.controller.buttonR1.pressed(self.wall_stake_mechanism.next_state)
        self.controller.buttonR2.pressed(self.wall_stake_mechanism.previous_state)

        self.controller.buttonY.pressed(
            lambda: self.log_and_print("Toggling corner mechanism") or self.corner_mechanism.toggle_corner_mechanism())
