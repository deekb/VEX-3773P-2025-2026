from VEXLib.Algorithms.TrapezoidProfile import TrapezoidProfile, Constraints
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation1d import Translation1d
from VEXLib.Util import time
from WallStakeMechanism import WallStakeState

from vex import PERCENT, DEGREES, Thread

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


def negative(robot):
    robot.mobile_goal_clamp.release_mobile_goal()

    # robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    # robot.wall_stake_mechanism.motor.spin_to_position(50, DEGREES, wait=False)

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-25), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-70), -30,
                                                          ramp_down=False)

    robot.mobile_goal_clamp.clamp_mobile_goal()
    # robot.scoring_mechanism.spin_motor_at_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), -30,
                                                          ramp_up=False,
                                                          turn_first=True)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(55), -85)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), -173)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-25), -173)

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(35), -150)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-50), -150)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), -210)


def positive(robot):
    robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    robot.wall_stake_mechanism.motor.spin_to_position(50, DEGREES, wait=False)

    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-32), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-80), 30,
                                                          ramp_down=False)

    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(45), 90)
    time.sleep(3)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(140), -90)


def drive_forwards(robot):
    time.sleep(10)

    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), 0)


def skills_alliance_stake(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(40, 30))

    robot.drivetrain.odometry.zero_rotation = Rotation2d.from_degrees(-90)
    # robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    # robot.wall_stake_mechanism.motor.spin_to_position(100, DEGREES, wait=False)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(37), -90)
    # robot.wall_stake_mechanism.motor.spin_to_position(200, DEGREES, wait=False)

    # robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-33), 90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-50), 0,
                                                          ramp_down=False)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    time.sleep(0.5)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(65), -87)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(62), 180)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), 85)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), 85)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), -140)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-10), -140)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-25), -60)
    time.sleep(1)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(27),
                                                          -55)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-190), 180)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(60), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(65), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), 90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), 90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-10), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-30), -135)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(10), -135)
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(50, 40))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(220), -105)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(80), -145)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(130), -25)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-130), -5)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-80), -30)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(0), 45)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(80, 60))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-100), 45)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(10), 45)


def new_skills_alliance_stake(robot: Robot):
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
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-43), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-55), 45)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(41), 45, turn_first=False, turn_correct=False)

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-185), -90)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(-100)
    stop_and_sleep(robot, 0.2)
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOADING)
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(70), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(79), 50)
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
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-50), -135)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.6, 2))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(75), -135)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(240), -70)
    robot.scoring_mechanism.spin_lower_intake(-100)
    schedule_function(1, lambda: robot.wall_stake_mechanism.transition_to(WallStakeState.LOW_SCORING))
    # robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.6, 5))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-500), -35)



def win_point(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.4))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-40), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(5), -90)
    robot.scoring_mechanism.intake()
    stop_and_sleep(robot, 0.25)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), -90)
    robot.scoring_mechanism.stop_motor()

    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.4))

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-90), 130)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    schedule_function(0.25, robot.scoring_mechanism.intake)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(55), -5)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(45), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), -165)


def positive_win_point(robot):
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
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(45), 5)
    time.sleep(1)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(30, 70))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(30), 160)


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


def positive_2_mobile_goal(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 100))
    robot.mobile_goal_clamp.release_mobile_goal()
    # robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    # robot.wall_stake_mechanism.motor.spin_to_position(200, DEGREES, wait=False)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(10), 0)
    robot.scoring_mechanism.set_speed(40)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(100), -40)
    robot.scoring_mechanism.set_speed(0)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 50))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-43), 180)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 100))
    robot.scoring_mechanism.set_speed(70)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(10), 180)
    time.sleep(0.35)
    robot.scoring_mechanism.set_speed(0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(25), 180)
    robot.mobile_goal_clamp.release_mobile_goal()
    time.sleep(0.5)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 30))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-50), -90)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(40), 50)


def win_point_states(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(40, 40))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), 0)
    robot.scoring_mechanism.spin_lower_intake(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(60), -45)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-48), 180)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    schedule_function(0.3, lambda: robot.scoring_mechanism.stop_motor())
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(15), 180)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), 180)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-55), -90)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    schedule_function(0.25, lambda: robot.scoring_mechanism.set_speed(100))
    if robot.alliance_color == "red":
        robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(60), 140)
        robot.mobile_goal_clamp.release_mobile_goal()
        robot.corner_mechanism.lower_corner_mechanism()
        robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), 140)
        robot.corner_mechanism.raise_corner_mechanism()
        robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), 140)


def second_win_point_states(robot):
    if robot.alliance_color == "red":
        robot.drivetrain.odometry.zero_rotation = Rotation2d.from_degrees(-130)
    elif robot.alliance_color == "blue":
        robot.drivetrain.odometry.zero_rotation = Rotation2d.from_degrees(130)

    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.4))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOADING)
    stop_and_sleep(robot, 0.2)
    robot.scoring_mechanism.set_speed(100)
    schedule_function(0.5, lambda: robot.scoring_mechanism.set_speed(-50))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(10), 130)
    robot.scoring_mechanism.stop_motor()
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOW_SCORING)
    stop_and_sleep(robot, 0.25)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-17), 130)
    robot.wall_stake_mechanism.transition_to(WallStakeState.DOCKED)
    stop_and_sleep(robot, 0.2)
    robot.scoring_mechanism.set_speed(100)
    schedule_function(0.3, lambda: robot.scoring_mechanism.intake_until_ring() or robot.scoring_mechanism.set_speed(
        100) or time.sleep(0.25) or robot.scoring_mechanism.intake_until_ring())
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), 55)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), 55)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-30), 55)
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-95), 135)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), 135)
    stop_and_sleep(robot, 0.25)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(85), -150)
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(75), -130)

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-70), -130)
    # robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-40), 40)
    # robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(70), 15)
    # robot.scoring_mechanism.spin_lower_intake(100)
    # schedule_function(0.5, lambda: robot.scoring_mechanism.stop_motor())
    schedule_function(0.2, lambda: robot.scoring_mechanism.intake_until_ring())
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), -45)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-35), 180)
    robot.mobile_goal_clamp.clamp_mobile_goal()


def third_win_point_states(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 2.125))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOADING)
    stop_and_sleep(robot, 0.2)
    robot.scoring_mechanism.set_speed(100)
    schedule_function(0.5, lambda: robot.scoring_mechanism.set_speed(-50))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(10), 130)
    robot.scoring_mechanism.stop_motor()
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOW_SCORING)
    stop_and_sleep(robot, 0.25)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-17), 130)
    robot.wall_stake_mechanism.transition_to(WallStakeState.DOCKED)
    robot.scoring_mechanism.set_speed(100)
    schedule_function(0.3, lambda: robot.scoring_mechanism.intake_until_ring() or robot.scoring_mechanism.intake_until_no_ring() or robot.scoring_mechanism.intake_until_ring())
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), 55)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), 55)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-30), 55)
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-85), 140)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    stop_and_sleep(robot, 0.5)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(5), -90)
    robot.scoring_mechanism.set_speed(-100)
    robot.mobile_goal_clamp.release_mobile_goal()
    schedule_function(0.2, robot.scoring_mechanism.intake_until_ring)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-43), 180)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    stop_and_sleep(robot, 0.1)
    robot.scoring_mechanism.spin_upper_intake(100)
    robot.scoring_mechanism.spin_lower_intake(-100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(120), 180)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-10), 180)
    robot.scoring_mechanism.set_speed(100)
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
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(55), 37)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-50), 37)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(65), 90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(40), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-105), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(60), 135)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), 135)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), 135)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-50), 135)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(120), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), -90)


def test_autonomous(robot):
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_meters(1), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_meters(1), 90)


def color_sort_test(robot):
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)


available_autos = [new_skills_alliance_stake, win_point_states, third_win_point_states, win_point, negative_4_rings_and_touch, color_sort_test, negative_full_mobile_goal]