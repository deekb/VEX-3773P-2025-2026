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
    def __init__(self, brain, autonomous):
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
            "red_negative_4_rings_and_touch": AutonomousRoutines.red_negative_4_rings_and_touch,
            "red_negative": AutonomousRoutines.red_negative,
            "red_positive": AutonomousRoutines.red_positive,
            "blue_negative": AutonomousRoutines.blue_negative,
            "blue_positive": AutonomousRoutines.blue_positive,
            "skills": AutonomousRoutines.skills,
            "red_win_point": AutonomousRoutines.red_win_point,
            "blue_win_point": AutonomousRoutines.blue_win_point,
        }

        self.autonomous = autonomous

    def debug_wait(self):
        while not self.controller.buttonA.pressing():
            pass
        while self.controller.buttonA.pressing():
            pass

    def on_autonomous(self):
        self.brain.screen.print("Autonomous: ")
        self.brain.screen.print(self.autonomous)
        self.autonomous_mappings[self.autonomous](self)

    def on_enable(self):
        self.drivetrain.odometry.inertial_sensor.set_rotation(0, DEGREES)
        self.drivetrain.left_drivetrain_PID.reset()
        self.drivetrain.right_drivetrain_PID.reset()
        self.drivetrain.set_speed_percent(0, 0)
        self.drivetrain.update_motor_voltages()

    def on_driver_control(self):
        self.wall_stake_mechanism.motor.set_velocity(0, PERCENT)
        self.wall_stake_mechanism.motor.spin(FORWARD)

    def on_setup(self):
        self.controller.buttonB.pressed(self.mobile_goal_clamp.toggle_clamp)
        self.controller.buttonY.pressed(self.doinker.toggle_corner_mechanism)
        self.controller.buttonR1.pressed(self.wall_stake_mechanism.start_scoring)
        self.controller.buttonR1.released(self.wall_stake_mechanism.stop)

        self.controller.buttonL1.pressed(self.wall_stake_mechanism.start_docking)
        self.controller.buttonL1.released(self.wall_stake_mechanism.stop)

        self.wall_stake_mechanism.calibrate()

    def driver_control_periodic(self):
        scoring_mechanism_speed = 0

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
