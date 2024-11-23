from VEXLib.Algorithms.TrapezoidProfile import TrapezoidProfile, Constraints
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation1d import Translation1d
from VEXLib.Util import time
from vex import PERCENT, DEGREES


def red_negative(robot):
    robot.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(90)
    robot.mobile_goal_clamp.release_mobile_goal()

    robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    robot.wall_stake_mechanism.motor.spin_to_position(50, DEGREES, wait=False)

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-25), 90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-70), 60, ramp_down=False)

    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.spin_motor_at_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), 60, ramp_up=False,
                                                         turn_first=True)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(55), 5)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), -83)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-25), -83)
    # robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(10), 0)

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(35), -60)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-50), -60)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), -120)


def blue_negative(robot):
    robot.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(-90)

    robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    robot.wall_stake_mechanism.motor.spin_to_position(50, DEGREES, wait=False)

    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-25), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-70), -60, ramp_down=False)

    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.spin_motor_at_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), -60, ramp_up=False)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(55), -5)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), 83)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-5), 83)


def red_positive(robot):
    robot.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(90)
    robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    robot.wall_stake_mechanism.motor.spin_to_position(50, DEGREES, wait=False)

    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-32), 90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-80), 120, ramp_down=False)

    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.spin_motor_at_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(45), 180)
    time.sleep(3)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(140), 0)


def blue_positive(robot):
    robot.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(-90)
    robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    robot.wall_stake_mechanism.motor.spin_to_position(50, DEGREES, wait=False)

    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-32), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-80), -120, ramp_down=False)

    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.spin_motor_at_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(45), -180)
    time.sleep(3)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(140), -0)


def skills(robot):
    robot.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(90)
    robot.mobile_goal_clamp.release_mobile_goal()
    # robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-7), 90)

    # robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), 90)
    # robot.wall_stake_mechanism.motor.spin_to_position(200, DEGREES, wait=False)
    # time.sleep(0.5)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-33), 90)
    robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    robot.wall_stake_mechanism.motor.spin_to_position(75, DEGREES, wait=True)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-60), 0)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.spin_motor_at_speed(100)
    time.sleep(0.5)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(70), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(70), 180)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(60), 85)
    time.sleep(1)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), 90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), -140)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-30), -60)
    time.sleep(3)
    robot.mobile_goal_clamp.release_mobile_goal()


def red_win_point(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(100, 90))
    robot.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(0)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    robot.wall_stake_mechanism.motor.spin_to_position(140, DEGREES, wait=False)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-38), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), -90)
    robot.wall_stake_mechanism.motor.spin_to_position(-300, DEGREES, wait=False)
    time.sleep(0.25)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), -90)
    robot.wall_stake_mechanism.motor.spin_to_position(200, DEGREES, wait=False)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-100), 125)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.spin_motor_at_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), 5)

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-10), 5)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(35), -80)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-10), -80)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), -45)


def blue_win_point(robot):
    robot.trapezoidal_profile = TrapezoidProfile(Constraints(50, 100))
    robot.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(0)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    robot.wall_stake_mechanism.motor.spin_to_position(140, DEGREES, wait=False)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-38), -0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), 90)
    robot.wall_stake_mechanism.motor.spin_to_position(-100, DEGREES, wait=False)
    time.sleep(0.5)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), 90)
    robot.wall_stake_mechanism.motor.spin_to_position(200, DEGREES, wait=False)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-100), -125)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.spin_motor_at_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), -5)
    # # time.sleep(1)
    # robot.scoring_mechanism.spin_motor_at_speed(-100)
    # time.sleep(0.25)
    # robot.scoring_mechanism.spin_motor_at_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(45), 80)
    # time.sleep(1)
    # robot.scoring_mechanism.spin_motor_at_speed(-100)
    # time.sleep(0.5)
    # robot.scoring_mechanism.spin_motor_at_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(80), -170)


def alliance_stake_test(robot):
    robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    robot.wall_stake_mechanism.motor.spin_to_position(110 + 100, DEGREES, wait=False)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-38), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), -90)
    robot.wall_stake_mechanism.motor.spin_to_position(-100 + 100, DEGREES, wait=False)
    time.sleep(0.5)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), -90)
    robot.wall_stake_mechanism.motor.spin_to_position(200 + 100, DEGREES, wait=False)


def println(robot, message):
    robot.brain.screen.print(message)
    robot.brain.screen.next_row()


def red_negative_4_rings_and_touch(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 100))
    robot.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(0)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    robot.wall_stake_mechanism.motor.spin_to_position(140, DEGREES, wait=False)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-38), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), -90)
    robot.wall_stake_mechanism.motor.spin_to_position(-300, DEGREES, wait=False)
    time.sleep(0.1)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), -90)
    robot.wall_stake_mechanism.motor.spin_to_position(200, DEGREES, wait=False)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 50))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-100), 125)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 100))
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.spin_motor_at_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), 5)

    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 500))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-10), 5)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(35), -80)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-10), -80)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), -45)
    robot.wall_stake_mechanism.motor.spin_to_position(0, DEGREES, wait=False)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-100), 0)