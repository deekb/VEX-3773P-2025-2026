from VEXLib.Robot.NewTickBasedRobot import TickBasedRobot
from Drivetrain import Drivetrain
from MobileGoalClamp import MobileGoalClamp
from ScoringMechanism import ScoringMechanism
from WallStakeMechanism import WallStakeMechanism
from CornerMechanism import CornerMechanism
from Constants import Preferences
import VEXLib.Math.MathUtil as MathUtil
import AutonomousRoutines
from vex import *


class Robot(TickBasedRobot):
    def __init__(self, brain):
        super().__init__(brain)
        self.controller = Controller(PRIMARY)
        self.drivetrain = Drivetrain()
        self.left_distance_sensor = Distance(Ports.PORT5)
        self.right_distance_sensor = Distance(Ports.PORT4)
        self.mobile_goal_clamp = MobileGoalClamp()
        self.scoring_mechanism = ScoringMechanism()
        self.wall_stake_mechanism = WallStakeMechanism()
        self.doinker = CornerMechanism()
        self.autonomous_mappings = {
            # "negative_4_rings_and_touch": AutonomousRoutines.negative_4_rings_and_touch,
            "negative": AutonomousRoutines.negative,
            "positive": AutonomousRoutines.positive,
            "win_point": AutonomousRoutines.win_point,
        }

        self.autonomous = lambda *args: None
        self.animation_thread = Thread(self.animation)

    def animation(self):
        i = 1

        while True:
            self.brain.screen.draw_image_from_file("/deploy/logo_vertical_frame_" + str(i) + ".png", 0, 0)
            wait(10, MSEC)
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
        self.drivetrain.odometry.inertial_sensor.set_rotation(0, DEGREES)
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
                wait(5, MSEC)

            if self.controller.buttonA.pressing():
                break

            if self.controller.buttonRight.pressing():
                selection_index += 1
            elif self.controller.buttonLeft.pressing():
                selection_index -= 1

            while self.controller.buttonRight.pressing() or self.controller.buttonLeft.pressing():
                wait(5, MSEC)

            if selection_index < 0:
                selection_index = 0
            elif selection_index >= len(options) - 1:
                selection_index = len(options) - 1

        return options[selection_index]

    def select_autonomous_routine(self):
        color = self.get_selection(["red", "blue", "skills"])
        while self.controller.buttonA.pressing():
            wait(5, MSEC)
        if color == "skills":
            self.drivetrain.set_angles_inverted(False)
            self.autonomous = AutonomousRoutines.skills
            return

        auto = self.get_selection(list(self.autonomous_mappings.keys()))

        self.drivetrain.set_angles_inverted(color == "blue")
        self.autonomous = self.autonomous_mappings[auto]

    def on_setup(self):
        self.select_autonomous_routine()

        self.controller.buttonB.pressed(self.mobile_goal_clamp.toggle_clamp)
        self.controller.buttonY.pressed(self.doinker.toggle_corner_mechanism)
        self.controller.buttonR1.pressed(self.wall_stake_mechanism.move_in)
        self.controller.buttonR1.released(self.wall_stake_mechanism.stop)

        self.controller.buttonL1.pressed(self.wall_stake_mechanism.move_out)
        self.controller.buttonL1.released(self.wall_stake_mechanism.stop)

        self.controller.buttonDown.pressed(self.wall_stake_mechanism.dock)
        self.controller.buttonRight.pressed(self.wall_stake_mechanism.score)

        self.wall_stake_mechanism.calibrate()

    def driver_control_periodic(self):
        scoring_mechanism_speed = 0

        # if self.controller.buttonUp.pressing():
        #     self.on_autonomous()

        if self.controller.buttonR2.pressing():
            scoring_mechanism_speed = 100
        elif self.controller.buttonL2.pressing():
            scoring_mechanism_speed = -100

        if Preferences.ARCADE_CONTROL:
            forward_speed = self.controller.axis3.position() / 100
            turn_speed = self.controller.axis4.position() / 100
            left_speed = forward_speed - turn_speed
            right_speed = forward_speed + turn_speed
        else:
            left_speed = self.controller.axis3.position() / 100
            right_speed = self.controller.axis2.position() / 100

        if Preferences.VOLTAGE_CONTROL:
            left_speed = MathUtil.apply_deadband(left_speed, 0.05, 1)
            right_speed = MathUtil.apply_deadband(right_speed, 0.05, 1)

            left_speed = MathUtil.cubic_filter(left_speed, linearity=0.4)
            right_speed = MathUtil.cubic_filter(right_speed, linearity=0.4)

            self.drivetrain.set_voltage(left_speed * 12, right_speed * 12)
        else:
            self.drivetrain.update_motor_voltages()

        if Preferences.PRINT_POSE:
            print(self.drivetrain.odometry.get_pose())

        self.drivetrain.update_odometry()
        self.wall_stake_mechanism.tick()
        self.scoring_mechanism.spin_motor_at_speed(scoring_mechanism_speed)
