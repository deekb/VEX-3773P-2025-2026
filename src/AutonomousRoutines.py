from VEXLib.Algorithms.TrapezoidProfile import TrapezoidProfile, Constraints
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation1d import Translation1d
from Drivetrain import TimeBasedCommand
from VEXLib.Geometry.Translation2d import Translation2d
from VEXLib.Util import time
from WallStakeMechanism import WallStakeState, WallStakeMechanism

from vex import DEGREES, Thread

# noinspection PyUnreachableCode
# For autocomplete only (would cause circular import)
if False:
    from Robot import Robot


def schedule_function(delay, callback):
    def function():
        time.sleep(delay)
        callback()

    Thread(function)


def stop_and_sleep(robot, time_to_sleep):
    start_time = time.time()
    while time.time() - start_time < time_to_sleep:
        robot.drivetrain.set_speed_zero_to_one(0, 0)
        robot.drivetrain.update_powers()


def bonk(robot):
    robot.wall_stake_mechanism.transition_to(WallStakeState.HIGH_SCORING)
    robot.wall_stake_mechanism.transition_to(WallStakeState.DOCKED)


def unload_if_didnt_score(robot):
    robot.wall_stake_mechanism.tick()
    while not robot.wall_stake_mechanism.at_setpoint():
        robot.wall_stake_mechanism.transition_to(WallStakeState.LOADING)
        robot.scoring_mechanism.set_speed(-100)
        stop_and_sleep(robot, 0.25)
        robot.wall_stake_mechanism.transition_to(WallStakeState.DOCKED)
        stop_and_sleep(robot, 0.5)


def drive_forwards(robot):
    time.sleep(10)

    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), 0)


def skills(robot: Robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.4, 1.4))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    stop_and_sleep(robot, 0.25)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(32), 0)
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-60), 90)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    stop_and_sleep(robot, 0.5)
    robot.scoring_mechanism.set_speed(100)
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOADING)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(60), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(81.5), -45)
    robot.scoring_mechanism.spin_upper_intake(-40)
    stop_and_sleep(robot, 0.2)
    robot.scoring_mechanism.spin_upper_intake(0)
    # schedule_function(0.7, lambda: robot.wall_stake_mechanism.transition_to(WallStakeState.HIGH_SCORING))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), -90)
    robot.wall_stake_mechanism.transition_to(WallStakeState.HIGH_SCORING)

    stop_and_sleep(robot, 0.25)

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-36), -90, turn_correct=False)

    unload_if_didnt_score(robot)

    robot.scoring_mechanism.set_speed(100)
    robot.wall_stake_mechanism.transition_to(WallStakeState.DOCKED)
    schedule_function(0.15, lambda: robot.scoring_mechanism.stop_motor())
    schedule_function(0.4, lambda: robot.scoring_mechanism.set_speed(100))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(100), 180)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(60), 180)

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-43), 180)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-36), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-55), 45)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(36), 45, turn_first=False, turn_correct=False)

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-185), -90)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(-100)
    stop_and_sleep(robot, 0.2)
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOADING)
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(70), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(75), 50)
    robot.scoring_mechanism.spin_upper_intake(-40)
    stop_and_sleep(robot, 0.2)
    robot.scoring_mechanism.spin_upper_intake(0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(55), 90)
    robot.wall_stake_mechanism.transition_to(WallStakeState.HIGH_SCORING)

    stop_and_sleep(robot, 0.5)

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-40), 90, turn_correct=False)

    unload_if_didnt_score(robot)

    robot.scoring_mechanism.set_speed(100)
    robot.wall_stake_mechanism.transition_to(WallStakeState.DOCKED)
    schedule_function(0.15, lambda: robot.scoring_mechanism.stop_motor())
    schedule_function(0.4, lambda: robot.scoring_mechanism.set_speed(100))

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(100), 180)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(60), 180)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-37), 180)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), 90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-30), 90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-52), -45)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.scoring_mechanism.set_speed(-100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(35), -45, turn_first=False, turn_correct=False)
    schedule_function(0.5, lambda: robot.scoring_mechanism.intake_until_ring())
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(190), 0)
    schedule_function(0.5, lambda: robot.scoring_mechanism.spin_lower_intake(100))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(80), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-75), 145)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(12), 135)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(130), 87)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), 87)
    # robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(40), 0)
    # robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-30), 0)
    robot.drivetrain.turn_to_gyro(-135)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-50), -135, turn_first=False)
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.6, 2))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(75), -135)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(240), -70)
    robot.scoring_mechanism.spin_lower_intake(-100)
    schedule_function(1, lambda: robot.wall_stake_mechanism.transition_to(WallStakeState.LOW_SCORING))
    # robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.6, 5))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-500), -35)


def negative_4_rings_and_touch(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.4))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-40), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(5), -90)
    robot.scoring_mechanism.intake()
    stop_and_sleep(robot, 0.25)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), -90)
    robot.wall_stake_mechanism.motor.spin_to_position(500, DEGREES, wait=False)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.4))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-90), 130)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.4))
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(55), -5)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(35), -90)

    # robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 500))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-10), -80)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(10), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), -45)
    # robot.wall_stake_mechanism.motor.spin_to_position(0, DEGREES, wait=False)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-15), -45)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.4))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(5), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-100), 0)


def win_point_states(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 2.125))
    robot.drivetrain.update_odometry()
    robot.drivetrain.rotation_PID.setpoint = robot.drivetrain.odometry.get_rotation().to_radians()
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOADING)
    stop_and_sleep(robot, 0.2)
    robot.scoring_mechanism.set_speed(100)
    schedule_function(1.0, lambda: robot.scoring_mechanism.set_speed(-20))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(10), 130)
    robot.scoring_mechanism.stop_motor()
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOW_SCORING)
    stop_and_sleep(robot, 0.25)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-17), 130)
    robot.wall_stake_mechanism.transition_to(WallStakeState.DOCKED)
    robot.scoring_mechanism.set_speed(100)
    schedule_function(0.3, lambda: robot.scoring_mechanism.intake_until_ring() or robot.scoring_mechanism.intake_until_no_ring() or robot.scoring_mechanism.intake_until_ring())
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(35), 55)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(45), 55)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-45), 55)  # Changed -30 to -45
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-85), 135)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    stop_and_sleep(robot, 0.5)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(5), -90)
    robot.scoring_mechanism.set_speed(-100)
    robot.mobile_goal_clamp.release_mobile_goal()
    schedule_function(0.2, robot.scoring_mechanism.intake_until_ring)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(45), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-43), 180)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    stop_and_sleep(robot, 0.1)
    robot.scoring_mechanism.spin_upper_intake(100)
    robot.scoring_mechanism.spin_lower_intake(-100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(120), 180)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-10), 180)
    robot.scoring_mechanism.set_speed(100)

    # Under this line was commented

    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(80), -135)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 2))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), -135)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), -135)
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOW_SCORING)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(145), 55)


def negative_full_mobile_goal(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.5))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-60), 180)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    stop_and_sleep(robot, 0.25)
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(58), 37)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-53), 37)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(65), 90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(40), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-105), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(60), 135)
    # robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), 135)
    # robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), 135)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-50), 135)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(120), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), -90)


def worlds_win_point(robot: Robot):
    if robot.alliance_color == "red":
        robot.corner_mechanism.set_left_side_active()
    else:
        robot.corner_mechanism.set_right_side_active()

    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.6, 3))
    # robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-15.0, 108.0))
    robot.corner_mechanism.toggle_active_corner_mechanism()
    stop_and_sleep(robot, 0.25)
    robot.scoring_mechanism.spin_lower_intake(100)
    robot.drivetrain.turn_to(Rotation2d.from_degrees(85))
    robot.corner_mechanism.toggle_active_corner_mechanism()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-30.0, 108.0))

    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-15.0, 108.0), use_back=True)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.6, 2.5))
    # stop_and_sleep(robot, 0.25)
    # robot.drivetrain.move_to_point(Translation2d.from_centimeters(-50.0, 106.0), use_back=True, mostly_there_command=robot.mobile_goal_clamp.clamp_mobile_goal, time_from_move_end=0.1)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-55.0, 106.0), use_back=True, commands=[TimeBasedCommand(-0.1, robot.mobile_goal_clamp.clamp_mobile_goal)])
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.6, 3))

    robot.mobile_goal_clamp.clamp_mobile_goal()
    # stop_and_sleep(robot, 0.3)
    robot.scoring_mechanism.set_speed(100)

    # schedule_function(0.3, lambda: robot.scoring_mechanism.intake_until_ring())

    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-45.0, 90.0))
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.6, 1.5))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-78.0, 103.0), use_back=True, commands=[TimeBasedCommand(0.1, robot.scoring_mechanism.intake_until_ring, background=True)])
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.6, 3))
    # stop_and_sleep(robot, 0.25)
    # robot.mobile_goal_clamp.clamp_mobile_goal()
    # stop_and_sleep(robot, 0.4)
    # robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.turn_to(Rotation2d.from_degrees(-120))
    # stop_and_sleep(robot, 0.85)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.scoring_mechanism.stop_motor()
    stop_and_sleep(robot, 0.25)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.6, 2.5))
    # robot.drivetrain.move_to_point(Translation2d.from_centimeters(-110.0, 72.0), use_back=True, mostly_there_command=robot.mobile_goal_clamp.clamp_mobile_goal, time_from_move_end=0.2)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-110.0, 72.0), use_back=True, commands=[TimeBasedCommand(-0.2, robot.mobile_goal_clamp.clamp_mobile_goal)])
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.6, 3))
    # robot.scoring_mechanism.set_speed(0)
    # stop_and_sleep(robot, 0.2)
    # robot.mobile_goal_clamp.clamp_mobile_goal()
    # stop_and_sleep(robot, 0.3)
    robot.scoring_mechanism.set_speed(100)
    # schedule_function(0.3, lambda: robot.scoring_mechanism.intake_until_ring() and robot.scoring_mechanism.eject_ring())
    # schedule_function(0.8, lambda: robot.scoring_mechanism.spin_lower_intake(-100))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(3.0, -30.0), stop_immediately=True)
    # robot.scoring_mechanism.back_off()
    # stop_and_sleep(robot, 0.2)
    robot.scoring_mechanism.set_speed(100)
    stop_and_sleep(robot, 0.3)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.6, 4))
    # robot.drivetrain.move_to_point(Translation2d.from_centimeters(-25.0, 12.0), use_back=True, turn=False)
    # robot.drivetrain.turn_to(Rotation2d.from_degrees(45))
    # stop_and_sleep(robot, 0.2)
    # robot.mobile_goal_clamp.release_mobile_goal()
    # stop_and_sleep(robot, 0.3)
    # robot.drivetrain.move_to_point(Translation2d.from_centimeters(-85.0, 95.0), use_back=True)
    # robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-129.0, 82.0), use_back=True, commands=[TimeBasedCommand(-0.2, robot.scoring_mechanism.stop_motor)])

    # schedule_function(1, lambda: robot.scoring_mechanism.stop_motor())


def ring_rush_eliminations(robot):
    robot.drivetrain.update_odometry()
    robot.drivetrain.rotation_PID.setpoint = robot.drivetrain.odometry.get_rotation().to_radians()
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 2 * 1.15))

    robot.ring_rush_mechanism.lower_ring_rush_mechanism()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(140), 39)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-39), 39, turn_first=False)
    robot.ring_rush_mechanism.raise_ring_rush_mechanism()
    stop_and_sleep(robot, 0.3)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(31), 125, commands=[TimeBasedCommand(0.1, robot.scoring_mechanism.intake_until_ring, background=True)])

    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.4, 1.5))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-59), 125, commands=[TimeBasedCommand(-0.1, robot.mobile_goal_clamp.clamp_mobile_goal)])
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 2 * 1.15))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(35), 70, commands=[TimeBasedCommand(-0.5, lambda: robot.scoring_mechanism.set_speed(100))])

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(25), 100)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.6, 3 * 1.15))

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(100), 180, commands=[TimeBasedCommand(0.8, lambda: robot.scoring_mechanism.spin_lower_intake(-100))])
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(55), 135, turn_correct=False)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), 135, turn_correct=False)

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(100), -85)
    robot.wall_stake_mechanism.transition_to(WallStakeState.HIGH_SCORING)

    # robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(130), -85, commands=[TimeBasedCommand(-0.8, lambda: robot.wall_stake_mechanism.transition_to(WallStakeState.HIGH_SCORING))])

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), -70)

    robot.wall_stake_mechanism.transition_to(WallStakeState.DOCKED)
    stop_and_sleep(robot, 0.3)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-10), -70)


def ring_rush_qualifications(robot):
    robot.drivetrain.update_odometry()
    robot.drivetrain.rotation_PID.setpoint = robot.drivetrain.odometry.get_rotation().to_radians()
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 2 * 1.15))

    robot.ring_rush_mechanism.lower_ring_rush_mechanism()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(140), 39)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-39), 39, turn_first=False)
    robot.ring_rush_mechanism.raise_ring_rush_mechanism()
    stop_and_sleep(robot, 0.3)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(31), 125, commands=[TimeBasedCommand(0.1, robot.scoring_mechanism.intake_until_ring, background=True)])

    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.4, 1.5))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-59), 125, commands=[TimeBasedCommand(-0.1, robot.mobile_goal_clamp.clamp_mobile_goal)])
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 2 * 1.15))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(35), 70, commands=[TimeBasedCommand(-0.5, lambda: robot.scoring_mechanism.set_speed(100))])

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(25), 100)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.6, 3 * 1.15))

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(100), 180, commands=[TimeBasedCommand(0.8, lambda: robot.scoring_mechanism.spin_lower_intake(-100))])
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(55), 135, turn_correct=False)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), 135, turn_correct=False)

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(120), -65)
    robot.ring_rush_mechanism.lower_ring_rush_mechanism()


def none(robot):
    robot.drivetrain.update_odometry()
    robot.drivetrain.rotation_PID.setpoint = robot.drivetrain.odometry.get_rotation().to_radians()
    robot.mobile_goal_clamp.release_mobile_goal()


def test_autonomous(robot):
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_meters(1), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_meters(1), 90)


def color_sort_test(robot):
    robot.mobile_goal_clamp.clamp_mobile_goal()
    stop_and_sleep(robot, 0.3)
    robot.scoring_mechanism.set_speed(100)


available_autos = [skills, win_point_states, negative_4_rings_and_touch, negative_full_mobile_goal, worlds_win_point, none, ring_rush_qualifications, ring_rush_eliminations, color_sort_test]
