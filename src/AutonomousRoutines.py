from VEXLib.Algorithms.TrapezoidProfile import TrapezoidProfile, Constraints
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation1d import Translation1d, Distance
from VEXLib.Util import time
from vex import PERCENT, DEGREES


def negative(robot):
    robot.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(0)
    robot.mobile_goal_clamp.release_mobile_goal()

    robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    robot.wall_stake_mechanism.motor.spin_to_position(50, DEGREES, wait=False)

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-25), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-70), -30, ramp_down=False)

    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.spin_motor_at_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), -30, ramp_up=False,
                                                          turn_first=True)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(55), -85)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), -173)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-25), -173)

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(35), -150)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-50), -150)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), -210)


def positive(robot):
    robot.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(0)
    robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    robot.wall_stake_mechanism.motor.spin_to_position(50, DEGREES, wait=False)

    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-32), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-80), 30, ramp_down=False)

    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.spin_motor_at_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(45), 90)
    time.sleep(3)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(140), -90)


def drive_forwards(robot):
    robot.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(0)
    time.sleep(10)

    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(12), 0)

def skills(robot):
    robot.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(90)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-33), 90)
    robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    robot.wall_stake_mechanism.motor.spin_to_position(75, DEGREES, wait=True)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-60), 0, ramp_down=False)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.spin_motor_at_speed(100)
    time.sleep(0.5)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(65), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(62), 180)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(80), 85)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), -140)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-30), -60)
    time.sleep(1)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(27),
                                                          -60)  # TODO: THIS IS THE DIAGONAL MOVE
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-190), 180)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(60), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(65), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(70), 90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-10), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-30), -135)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(10), -135)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(220), -105)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(80), -145)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(130), -25)


def win_point(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 70))
    robot.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(0)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    robot.wall_stake_mechanism.motor.spin_to_position(140, DEGREES, wait=False)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-38), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), -90)
    robot.wall_stake_mechanism.motor.spin_to_position(-300, DEGREES, wait=False)
    time.sleep(0.25)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), -90)
    robot.wall_stake_mechanism.motor.spin_to_position(300, DEGREES, wait=False)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 30))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-90), 130)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 70))
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.spin_motor_at_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(45), -5)

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(35), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), -90, ramp_up=False,
                                                          ramp_down=False)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), -165, ramp_up=False,
                                                          ramp_down=False)

def positive_win_point(robot):
    robot.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(0)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    robot.wall_stake_mechanism.motor.spin_to_position(140, DEGREES, wait=False)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-38), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), 90)
    robot.wall_stake_mechanism.motor.spin_to_position(-300, DEGREES, wait=False)
    time.sleep(0.25)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), 90)
    robot.wall_stake_mechanism.motor.spin_to_position(300, DEGREES, wait=False)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 30))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-90), -130)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 70))
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.spin_motor_at_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(45), 5)
    time.sleep(1)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(30, 70))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(30), 160)

def println(robot, message):
    robot.brain.screen.print(message)
    robot.brain.screen.next_row()


def negative_4_rings_and_touch(robot):
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

def test_autonomous(robot):
    robot.drivetrain.move_distance_towards_direction_trap_corrected(Translation1d.from_centimeters(100), 0)
    robot.drivetrain.move_distance_towards_direction_trap_corrected(Translation1d.from_centimeters(100), 90)
    robot.drivetrain.move_distance_towards_direction_trap_corrected(Translation1d.from_centimeters(100), 180)
    robot.drivetrain.move_distance_towards_direction_trap_corrected(Translation1d.from_centimeters(100), 270)