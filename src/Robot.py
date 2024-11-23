import json

from VEXLib.Algorithms.TrapezoidProfile import TrapezoidProfile, Constraints
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation2d import Translation2d
from VEXLib.Geometry.Translation1d import Translation1d
from VEXLib.Robot.TelemteryRobot import TelemetryRobot
from VEXLib.Robot.NewTickBasedRobot import TickBasedRobot
from VEXLib.Util import time
from Drivetrain import Drivetrain
from MobileGoalClamp import MobileGoalClamp
from ScoringMechanism import ScoringMechanism
from WallStakeMechanism import WallStakeMechanism
from CornerMechanism import CornerMechanism
from Constants import Preferences
from SerialData import Frame
from CRC import crc_bytes
import VEXLib.Math.MathUtil as MathUtil
from vex import *


class Robot(TickBasedRobot):
    def __init__(self, brain, autonomous):
        super().__init__(brain)
        self.controller = Controller(PRIMARY)
        self.drivetrain = Drivetrain()
        self.left_distance_sensor = Distance(Ports.PORT5)
        self.right_distance_sensor = Distance(Ports.PORT4)
        self.i = 0
        self.mobile_goal_clamp = MobileGoalClamp()
        self.scoring_mechanism = ScoringMechanism()
        self.wall_stake_mechanism = WallStakeMechanism()
        self.doinker = CornerMechanism()
        self.autonomous = autonomous

    def debug_wait(self):
        while not self.controller.buttonA.pressing():
            pass
        while self.controller.buttonA.pressing():
            pass

    def red_negative(self):
        self.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(90)
        self.mobile_goal_clamp.release_mobile_goal()

        self.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
        self.wall_stake_mechanism.motor.spin_to_position(50, DEGREES, wait=False)

        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-25), 90)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-70), 60, ramp_down=False)

        self.mobile_goal_clamp.clamp_mobile_goal()
        self.scoring_mechanism.spin_motor_at_speed(100)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), 60, ramp_up=False, turn_first=True)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(55), 5)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), -83)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-25), -83)
        # self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(10), 0)


        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(35), -60)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-50), -60)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), -120)

    def blue_negative(self):
        self.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(-90)

        self.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
        self.wall_stake_mechanism.motor.spin_to_position(50, DEGREES, wait=False)

        self.mobile_goal_clamp.release_mobile_goal()
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-25), -90)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-70), -60, ramp_down=False)

        self.mobile_goal_clamp.clamp_mobile_goal()
        self.scoring_mechanism.spin_motor_at_speed(100)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), -60, ramp_up=False)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(55), -5)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), 83)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-5), 83)

    def red_positive(self):
        self.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(90)
        self.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
        self.wall_stake_mechanism.motor.spin_to_position(50, DEGREES, wait=False)

        self.mobile_goal_clamp.release_mobile_goal()
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-32), 90)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-80), 120, ramp_down=False)

        self.mobile_goal_clamp.clamp_mobile_goal()
        self.scoring_mechanism.spin_motor_at_speed(100)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(45), 180)
        time.sleep(3)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(140), 0)

    def blue_positive(self):
        self.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(-90)
        self.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
        self.wall_stake_mechanism.motor.spin_to_position(50, DEGREES, wait=False)

        self.mobile_goal_clamp.release_mobile_goal()
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-32), -90)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-80), -120, ramp_down=False)

        self.mobile_goal_clamp.clamp_mobile_goal()
        self.scoring_mechanism.spin_motor_at_speed(100)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(45), -180)
        time.sleep(3)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(140), -0)

    def skills(self):
        self.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(90)
        self.mobile_goal_clamp.release_mobile_goal()
        # self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-7), 90)

        # self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), 90)
        # self.wall_stake_mechanism.motor.spin_to_position(200, DEGREES, wait=False)
        # time.sleep(0.5)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-33), 90)
        self.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
        self.wall_stake_mechanism.motor.spin_to_position(75, DEGREES, wait=True)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-60), 0)
        self.mobile_goal_clamp.clamp_mobile_goal()
        self.scoring_mechanism.spin_motor_at_speed(100)
        time.sleep(0.5)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(70), -90)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(70), 180)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(60), 85)
        time.sleep(1)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), 90)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), -140)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-30), -60)
        time.sleep(3)
        self.mobile_goal_clamp.release_mobile_goal()

    def red_win_point(self):
        self.println("1")
        self.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(100, 90))
        self.println("2")
        self.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(0)
        self.println("3")
        self.mobile_goal_clamp.release_mobile_goal()
        self.println("4")
        self.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
        self.println("5")
        self.wall_stake_mechanism.motor.spin_to_position(140, DEGREES, wait=False)
        self.println("6")
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-38), 0)
        self.println("7")
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), -90)
        self.println("8")
        self.wall_stake_mechanism.motor.spin_to_position(-300, DEGREES, wait=False)
        self.println("9")
        time.sleep(0.25)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), -90)
        self.wall_stake_mechanism.motor.spin_to_position(200, DEGREES, wait=False)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-100), 125)
        self.mobile_goal_clamp.clamp_mobile_goal()
        self.scoring_mechanism.spin_motor_at_speed(100)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), 5)

        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-10), 5)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(35), -80)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-10), -80)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), -45)

    def blue_win_point(self):
        self.trapezoidal_profile = TrapezoidProfile(Constraints(50, 100))
        self.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(0)
        self.mobile_goal_clamp.release_mobile_goal()
        self.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
        self.wall_stake_mechanism.motor.spin_to_position(140, DEGREES, wait=False)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-38), -0)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), 90)
        self.wall_stake_mechanism.motor.spin_to_position(-100, DEGREES, wait=False)
        time.sleep(0.5)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), 90)
        self.wall_stake_mechanism.motor.spin_to_position(200, DEGREES, wait=False)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-100), -125)
        self.mobile_goal_clamp.clamp_mobile_goal()
        self.scoring_mechanism.spin_motor_at_speed(100)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), -5)
        # # time.sleep(1)
        # self.scoring_mechanism.spin_motor_at_speed(-100)
        # time.sleep(0.25)
        # self.scoring_mechanism.spin_motor_at_speed(100)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(45), 80)
        # time.sleep(1)
        # self.scoring_mechanism.spin_motor_at_speed(-100)
        # time.sleep(0.5)
        # self.scoring_mechanism.spin_motor_at_speed(100)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(80), -170)

    def alliance_stake_test(self):
        self.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
        self.wall_stake_mechanism.motor.spin_to_position(110+100, DEGREES, wait=False)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-38), 0)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), -90)
        self.wall_stake_mechanism.motor.spin_to_position(-100+100, DEGREES, wait=False)
        time.sleep(0.5)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), -90)
        self.wall_stake_mechanism.motor.spin_to_position(200+100, DEGREES, wait=False)

    def println(self, message):
        self.brain.screen.print(message)
        self.brain.screen.next_row()

    def red_negative_4_rings_and_touch(self):
        self.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 100))
        self.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(0)
        self.mobile_goal_clamp.release_mobile_goal()
        self.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
        self.wall_stake_mechanism.motor.spin_to_position(140, DEGREES, wait=False)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-38), 0)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), -90)
        self.wall_stake_mechanism.motor.spin_to_position(-300, DEGREES, wait=False)
        time.sleep(0.1)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), -90)
        self.wall_stake_mechanism.motor.spin_to_position(200, DEGREES, wait=False)
        self.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 50))
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-100), 125)
        self.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 100))
        self.mobile_goal_clamp.clamp_mobile_goal()
        self.scoring_mechanism.spin_motor_at_speed(100)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), 5)

        self.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 500))
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-10), 5)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(35), -80)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-10), -80)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), -45)
        self.wall_stake_mechanism.motor.spin_to_position(0, DEGREES, wait=False)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-100), 0)

    def on_autonomous(self):
        self.brain.screen.print("Autonomous: ")
        self.brain.screen.print(self.autonomous)
        if "red_negative" in self.autonomous:
            self.red_negative()
        if "red_positive" in self.autonomous:
            self.red_positive()
        if "blue_negative" in self.autonomous:
            self.blue_negative()
        if "blue_positive" in self.autonomous:
            self.blue_positive()
        if "skills" in self.autonomous:
            self.skills()
        if "red_win_point" in self.autonomous:
            self.println("RWP")
            self.red_win_point()
        if "blue_win_point" in self.autonomous:
            self.blue_win_point()
        if "red_negative_4_rings_and_touch" in self.autonomous:
            self.red_negative_4_rings_and_touch()

    def on_enable(self):
        self.drivetrain.odometry.inertial_sensor.set_rotation(0, DEGREES)
        self.drivetrain.left_drivetrain_PID.reset()
        self.drivetrain.right_drivetrain_PID.reset()
        self.drivetrain.set_speed_percent(0, 0)

    def on_driver_control(self):
        self.wall_stake_mechanism.motor.set_velocity(0, PERCENT)
        self.wall_stake_mechanism.motor.spin(FORWARD)

    def on_setup(self):
        # self.register_telemetry()
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

        left_speed = MathUtil.apply_deadband(left_speed, 0.05, 1)
        right_speed = MathUtil.apply_deadband(right_speed, 0.05, 1)

        left_speed = MathUtil.cubic_filter(left_speed, linearity=0.4)
        right_speed = MathUtil.cubic_filter(right_speed, linearity=0.4)

        self.drivetrain.set_voltage(left_speed * 12, right_speed * 12)

        # self.drivetrain.update_motor_voltages()
        self.drivetrain.update_odometry()

        if Preferences.PRINT_POSE:
            print(self.drivetrain.odometry.get_pose())

        self.wall_stake_mechanism.tick()

        self.scoring_mechanism.spin_motor_at_speed(scoring_mechanism_speed)
