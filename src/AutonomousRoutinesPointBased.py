import WallStakeMechanism as WallStakeMechanism
from VEXLib.Algorithms.TrapezoidProfile import TrapezoidProfile, Constraints
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation2d import Translation2d
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
    robot.wall_stake_mechanism.transition_to(WallStakeMechanism.WallStakeState.HIGH_SCORING)
    robot.wall_stake_mechanism.transition_to(WallStakeMechanism.WallStakeState.DOCKED)


def unload_if_didnt_score(robot):
    robot.wall_stake_mechanism.tick()
    while not robot.wall_stake_mechanism.at_setpoint():
        robot.wall_stake_mechanism.transition_to(WallStakeState.LOADING)
        robot.scoring_mechanism.set_speed(-100)
        stop_and_sleep(robot, 0.25)
        robot.wall_stake_mechanism.transition_to(WallStakeState.DOCKED)
        stop_and_sleep(robot, 0.5)


def negative_point_based(robot):
    robot.mobile_goal_clamp.release_mobile_goal()

    # robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    # robot.wall_stake_mechanism.motor.spin_to_position(50, DEGREES, wait=False)

    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-25.0, 0.0), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-85.622, 35.0), use_back=True)

    robot.mobile_goal_clamp.clamp_mobile_goal()
    # robot.scoring_mechanism.spin_motor_at_speed(100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-102.942, 45.0), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-98.149, -9.791))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-127.925, -13.447))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-103.111, -10.4), use_back=True)

    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-133.422, -27.9))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-90.121, -2.9), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-133.422, 22.1))


def positive_point_based(robot):
    robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    robot.wall_stake_mechanism.motor.spin_to_position(50, DEGREES, wait=False)

    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-32.0, 0.0), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-101.282, -40.0), use_back=True)

    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-101.282, 5.0))
    time.sleep(3)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-101.282, -135.0))


def drive_forwards_point_based(robot):
    time.sleep(10)

    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(30.0, 0.0))


def skills_alliance_stake_point_based(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(40, 30))

    robot.drivetrain.odometry.zero_rotation = Rotation2d.from_degrees(-90)
    # robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    # robot.wall_stake_mechanism.motor.spin_to_position(100, DEGREES, wait=False)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-0.0, 20.0), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(0.0, -17.0))
    # robot.wall_stake_mechanism.motor.spin_to_position(200, DEGREES, wait=False)

    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-0.0, -50.0), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-50.0, -50.0), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    time.sleep(0.5)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-46.598, -114.911))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-108.598, -114.911))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-104.24, -65.101))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-101.626, -35.215))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-124.607, -54.499))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-116.947, -48.071), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-129.447, -26.42), use_back=True)
    time.sleep(1)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-113.96, -48.538))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(76.04, -48.538), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(76.04, -108.538))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(141.04, -108.538))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(141.04, -58.538))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(141.04, -28.538))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(161.04, -28.538))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(151.04, -28.538), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(172.253, -7.324), use_back=True)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(165.182, -14.395))
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(50, 40))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(108.242, -226.899))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(42.71, -272.785))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(160.53, -327.726))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(31.024, -316.395), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-38.258, -276.395), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-38.258, -276.395))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(80, 60))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-108.968, -347.106), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-101.897, -340.035))


def new_skills_alliance_stake_point_based(robot: Robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.4, 1.4))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    stop_and_sleep(robot, 0.25)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(32.0, 0.0))
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(32.0, -60.0), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    stop_and_sleep(robot, 0.5)
    robot.scoring_mechanism.set_speed(100)
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOADING)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(92.0, -60.0))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(149.629, -117.629))
    robot.scoring_mechanism.spin_upper_intake(-40)
    stop_and_sleep(robot, 0.2)
    robot.scoring_mechanism.spin_upper_intake(0)
    # schedule_function(0.7, lambda: robot.wall_stake_mechanism.transition_to(WallStakeState.HIGH_SCORING))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(149.629, -167.629))
    robot.wall_stake_mechanism.transition_to(WallStakeState.HIGH_SCORING)

    stop_and_sleep(robot, 0.25)

    robot.drivetrain.move_to_point(Translation2d.from_centimeters(149.629, -131.629), use_back=True)

    unload_if_didnt_score(robot)

    robot.scoring_mechanism.set_speed(100)
    robot.wall_stake_mechanism.transition_to(WallStakeState.DOCKED)
    schedule_function(0.15, lambda: robot.scoring_mechanism.stop_motor())
    schedule_function(0.4, lambda: robot.scoring_mechanism.set_speed(100))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(49.629, -131.629))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-10.371, -131.629))

    robot.drivetrain.move_to_point(Translation2d.from_centimeters(32.629, -131.629), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(32.629, -161.629))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(32.629, -118.629), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-6.262, -157.52), use_back=True)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(22.73, -128.529))

    robot.drivetrain.move_to_point(Translation2d.from_centimeters(22.73, 56.471), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(-100)
    stop_and_sleep(robot, 0.2)
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOADING)
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(92.73, 56.471))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(143.51, 116.989))
    robot.scoring_mechanism.spin_upper_intake(-40)
    stop_and_sleep(robot, 0.2)
    robot.scoring_mechanism.spin_upper_intake(0)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(143.51, 171.989))
    robot.wall_stake_mechanism.transition_to(WallStakeState.HIGH_SCORING)

    stop_and_sleep(robot, 0.5)

    robot.drivetrain.move_to_point(Translation2d.from_centimeters(143.51, 131.989), use_back=True)

    unload_if_didnt_score(robot)

    robot.scoring_mechanism.set_speed(100)
    robot.wall_stake_mechanism.transition_to(WallStakeState.DOCKED)
    schedule_function(0.15, lambda: robot.scoring_mechanism.stop_motor())
    schedule_function(0.4, lambda: robot.scoring_mechanism.set_speed(100))

    robot.drivetrain.move_to_point(Translation2d.from_centimeters(43.51, 131.989))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-16.49, 131.989))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(20.51, 131.989), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(20.51, 161.989))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(20.51, 131.989), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-16.26, 168.758), use_back=True)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.scoring_mechanism.set_speed(-100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(8.489, 144.01))
    schedule_function(0.5, lambda: robot.scoring_mechanism.intake_until_ring())
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(198.489, 144.01))
    schedule_function(0.5, lambda: robot.scoring_mechanism.spin_lower_intake(100))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(198.489, 64.01))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(259.926, 20.991), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(251.44, 29.477))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(258.244, 159.299))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(257.197, 139.326), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(297.197, 139.326))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(267.197, 139.326), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(302.553, 174.681), use_back=True)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.6, 2))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(249.52, 121.648))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(331.604, -103.878))
    robot.scoring_mechanism.spin_lower_intake(-100)
    schedule_function(1, lambda: robot.wall_stake_mechanism.transition_to(WallStakeState.LOW_SCORING))
    # robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.6, 5))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-77.972, 182.91), use_back=True)


def win_point_point_based(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.4))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-40.0, 0.0), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-40.0, 20.0), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-40.0, 15.0))
    robot.scoring_mechanism.intake()
    stop_and_sleep(robot, 0.25)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-40.0, -5.0))
    robot.scoring_mechanism.stop_motor()

    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.4))

    robot.drivetrain.move_to_point(Translation2d.from_centimeters(17.851, -73.944), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    schedule_function(0.25, robot.scoring_mechanism.intake)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(72.642, -78.738))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(72.642, -123.738))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(72.642, -103.738), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(24.345, -116.679))


def positive_win_point_point_based(robot):
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    robot.wall_stake_mechanism.motor.spin_to_position(140, DEGREES, wait=False)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-38.0, 0.0), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-38.0, -20.0), use_back=True)
    robot.wall_stake_mechanism.motor.spin_to_position(-300, DEGREES, wait=False)
    time.sleep(0.25)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-38.0, 0.0))
    robot.wall_stake_mechanism.motor.spin_to_position(300, DEGREES, wait=False)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 30))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(19.851, 68.944), use_back=True)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 70))
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(64.68, 72.866))
    time.sleep(1)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(30, 70))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-6.925, 98.928))


def negative_4_rings_and_touch_point_based(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.4))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-40.0, 0.0), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-40.0, 20.0), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-40.0, 15.0))
    robot.scoring_mechanism.intake()
    stop_and_sleep(robot, 0.25)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-40.0, -5.0))
    robot.wall_stake_mechanism.motor.spin_to_position(500, DEGREES, wait=False)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.4))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(17.851, -73.944), use_back=True)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.4))
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(72.642, -78.738))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(72.642, -113.738))

    # robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 500))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(70.905, -103.889), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(80.905, -103.889))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(95.047, -118.032))
    # robot.wall_stake_mechanism.motor.spin_to_position(0, DEGREES, wait=False)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(84.441, -107.425), use_back=True)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.4))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(89.441, -107.425))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-10.559, -107.425), use_back=True)


def positive_2_mobile_goal_point_based(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 100))
    robot.mobile_goal_clamp.release_mobile_goal()
    # robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    # robot.wall_stake_mechanism.motor.spin_to_position(200, DEGREES, wait=False)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(10.0, 0.0))
    robot.scoring_mechanism.set_speed(40)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(86.604, -64.279))
    robot.scoring_mechanism.set_speed(0)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 50))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(129.604, -64.279), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 100))
    robot.scoring_mechanism.set_speed(70)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(119.604, -64.279))
    time.sleep(0.35)
    robot.scoring_mechanism.set_speed(0)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(94.604, -64.279))
    robot.mobile_goal_clamp.release_mobile_goal()
    time.sleep(0.5)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 30))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(94.604, -14.279), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(120.316, 16.363))


def win_point_states_point_based(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(40, 40))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(50.0, 0.0))
    robot.scoring_mechanism.spin_lower_intake(100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(92.426, -42.426))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(140.426, -42.426), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    schedule_function(0.3, lambda: robot.scoring_mechanism.stop_motor())
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(125.426, -42.426))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(105.426, -42.426))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(105.426, 12.574), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    schedule_function(0.25, lambda: robot.scoring_mechanism.set_speed(100))
    if robot.alliance_color == "red":
        robot.drivetrain.move_to_point(Translation2d.from_centimeters(59.464, 51.141))
        robot.mobile_goal_clamp.release_mobile_goal()
        robot.corner_mechanism.lower_corner_mechanism()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(74.785, 38.285), use_back=True)
    robot.corner_mechanism.raise_corner_mechanism()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(51.803, 57.569))


def second_win_point_states_point_based(robot):
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
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-6.428, 7.66))
    robot.scoring_mechanism.stop_motor()
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOW_SCORING)
    stop_and_sleep(robot, 0.25)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(4.5, -5.362), use_back=True)
    robot.wall_stake_mechanism.transition_to(WallStakeState.DOCKED)
    stop_and_sleep(robot, 0.2)
    robot.scoring_mechanism.set_speed(100)
    schedule_function(0.3, lambda: robot.scoring_mechanism.intake_until_ring() or robot.scoring_mechanism.set_speed(
        100) or time.sleep(0.25) or robot.scoring_mechanism.intake_until_ring())
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(21.707, 19.212))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(50.386, 60.17))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(33.178, 35.595), use_back=True)
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(100.353, -31.58), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(86.211, -17.438))
    stop_and_sleep(robot, 0.25)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(12.599, -59.938))
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(12.599, -109.938))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-35.61, -167.391))

    robot.drivetrain.move_to_point(Translation2d.from_centimeters(9.385, -113.768), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-21.257, -139.479), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(46.358, -121.362))
    # robot.scoring_mechanism.spin_lower_intake(100)
    # schedule_function(0.5, lambda: robot.scoring_mechanism.stop_motor())
    schedule_function(0.2, lambda: robot.scoring_mechanism.intake_until_ring())
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(81.714, -156.717))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(116.714, -156.717), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()


def third_win_point_states_point_based(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 2.125))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOADING)
    stop_and_sleep(robot, 0.2)
    robot.scoring_mechanism.set_speed(100)
    schedule_function(0.5, lambda: robot.scoring_mechanism.set_speed(-50))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-6.428, 7.66))
    robot.scoring_mechanism.stop_motor()
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOW_SCORING)
    stop_and_sleep(robot, 0.25)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(4.5, -5.362), use_back=True)
    robot.wall_stake_mechanism.transition_to(WallStakeState.DOCKED)
    robot.scoring_mechanism.set_speed(100)
    schedule_function(0.3,
                      lambda: robot.scoring_mechanism.intake_until_ring() or robot.scoring_mechanism.intake_until_no_ring() or robot.scoring_mechanism.intake_until_ring())
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(21.707, 19.212))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(50.386, 60.17))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(33.178, 35.595), use_back=True)
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(98.292, -19.042), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    stop_and_sleep(robot, 0.5)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(98.292, -24.042))
    robot.scoring_mechanism.set_speed(-100)
    robot.mobile_goal_clamp.release_mobile_goal()
    schedule_function(0.2, robot.scoring_mechanism.intake_until_ring)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(98.292, -74.042))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(141.292, -74.042), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    stop_and_sleep(robot, 0.1)
    robot.scoring_mechanism.spin_upper_intake(100)
    robot.scoring_mechanism.spin_lower_intake(-100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(21.292, -74.042))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(31.292, -74.042), use_back=True)
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-25.276, -130.61))
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 2))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-11.134, -116.468), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(3.008, -102.326), use_back=True)
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOW_SCORING)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(86.176, 16.451))


def negative_full_mobile_goal_point_based(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.5))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(60.0, -0.0), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    stop_and_sleep(robot, 0.25)
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(103.925, 33.1))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(63.993, 3.009), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(63.993, 68.009))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(103.993, 68.009))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-1.007, 68.009), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-43.433, 110.435))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-29.291, 96.293), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-50.504, 117.507))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-15.149, 82.151), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-15.149, -37.849))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-15.149, -67.849))


def test_autonomous_point_based(robot):
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(100.0, 0.0))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(100.0, 100.0))


# available_autos = [new_skills_alliance_stake_point_based, win_point_states_point_based, third_win_point_states_point_based, win_point_point_based, negative_4_rings_and_touch_point_based, negative_full_mobile_goal_point_based, test_autonomous_point_basednew_skills_alliance_stake_point_based, win_point_states_point_based, third_win_point_states_point_based, win_point_point_based, negative_4_rings_and_touch_point_based, negative_full_mobile_goal_point_based, test_autonomous_point_based]
available_autos = []
