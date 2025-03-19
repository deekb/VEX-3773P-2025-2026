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


def negative(robot):
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


def positive(robot):
    robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    robot.wall_stake_mechanism.motor.spin_to_position(50, DEGREES, wait=False)

    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-165.422, 22.1), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-234.704, -17.9), use_back=True)

    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-234.704, 27.1))
    time.sleep(3)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-234.704, -112.9))


def drive_forwards(robot):
    time.sleep(10)

    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-204.704, -112.9))


def skills_alliance_stake(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(40, 30))

    robot.drivetrain.odometry.zero_rotation = Rotation2d.from_degrees(-90)
    # robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    # robot.wall_stake_mechanism.motor.spin_to_position(100, DEGREES, wait=False)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-204.704, -92.9), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-204.704, -129.9))
    # robot.wall_stake_mechanism.motor.spin_to_position(200, DEGREES, wait=False)

    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-204.704, -162.9), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-254.704, -162.9), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    time.sleep(0.5)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-251.303, -227.811))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-313.303, -227.811))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-308.945, -178.001))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-306.33, -148.115))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-329.311, -167.399))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-321.651, -160.971), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-334.151, -139.321), use_back=True)
    time.sleep(1)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-318.664, -161.438))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-128.664, -161.438), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-128.664, -221.438))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-63.664, -221.438))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-63.664, -171.438))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-63.664, -141.438))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-43.664, -141.438))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-53.664, -141.438), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-32.451, -120.224), use_back=True)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-39.522, -127.295))
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(50, 40))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-96.462, -339.799))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-161.995, -385.685))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-44.175, -440.626))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-173.68, -429.295), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-242.962, -389.295), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-242.962, -389.295))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(80, 60))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-313.673, -460.006), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-306.602, -452.935))


def new_skills_alliance_stake(robot: Robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.4, 1.4))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    stop_and_sleep(robot, 0.25)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-274.602, -452.935))
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-274.602, -512.935), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    stop_and_sleep(robot, 0.5)
    robot.scoring_mechanism.set_speed(100)
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOADING)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-214.602, -512.935))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-156.972, -570.564))
    robot.scoring_mechanism.spin_upper_intake(-40)
    stop_and_sleep(robot, 0.2)
    robot.scoring_mechanism.spin_upper_intake(0)
    # schedule_function(0.7, lambda: robot.wall_stake_mechanism.transition_to(WallStakeState.HIGH_SCORING))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-156.972, -620.564))
    robot.wall_stake_mechanism.transition_to(WallStakeState.HIGH_SCORING)

    stop_and_sleep(robot, 0.25)

    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-156.972, -584.564), use_back=True)

    unload_if_didnt_score(robot)

    robot.scoring_mechanism.set_speed(100)
    robot.wall_stake_mechanism.transition_to(WallStakeState.DOCKED)
    schedule_function(0.15, lambda: robot.scoring_mechanism.stop_motor())
    schedule_function(0.4, lambda: robot.scoring_mechanism.set_speed(100))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-256.972, -584.564))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-316.972, -584.564))

    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-273.972, -584.564), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-273.972, -614.564))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-273.972, -571.564), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-312.863, -610.455), use_back=True)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-283.872, -581.464))

    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-283.872, -396.464), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(-100)
    stop_and_sleep(robot, 0.2)
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOADING)
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-213.872, -396.464))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-163.092, -335.946))
    robot.scoring_mechanism.spin_upper_intake(-40)
    stop_and_sleep(robot, 0.2)
    robot.scoring_mechanism.spin_upper_intake(0)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-163.092, -280.946))
    robot.wall_stake_mechanism.transition_to(WallStakeState.HIGH_SCORING)

    stop_and_sleep(robot, 0.5)

    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-163.092, -320.946), use_back=True)

    unload_if_didnt_score(robot)

    robot.scoring_mechanism.set_speed(100)
    robot.wall_stake_mechanism.transition_to(WallStakeState.DOCKED)
    schedule_function(0.15, lambda: robot.scoring_mechanism.stop_motor())
    schedule_function(0.4, lambda: robot.scoring_mechanism.set_speed(100))

    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-263.092, -320.946))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-323.092, -320.946))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-286.092, -320.946), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-286.092, -290.946))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-286.092, -320.946), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-322.861, -284.177), use_back=True)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.scoring_mechanism.set_speed(-100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-298.112, -308.925))
    schedule_function(0.5, lambda: robot.scoring_mechanism.intake_until_ring())
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-108.112, -308.925))
    schedule_function(0.5, lambda: robot.scoring_mechanism.spin_lower_intake(100))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-108.112, -388.925))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-46.676, -431.944), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-55.161, -423.458))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-48.358, -293.637))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-49.404, -313.609), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-9.404, -313.609))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-39.404, -313.609), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-4.049, -278.254), use_back=True)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.6, 2))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-57.082, -331.287))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(25.003, -556.813))
    robot.scoring_mechanism.spin_lower_intake(-100)
    schedule_function(1, lambda: robot.wall_stake_mechanism.transition_to(WallStakeState.LOW_SCORING))
    # robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.6, 5))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-384.573, -270.025), use_back=True)


def win_point(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.4))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-424.573, -270.025), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-424.573, -250.025), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-424.573, -255.025))
    robot.scoring_mechanism.intake()
    stop_and_sleep(robot, 0.25)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-424.573, -275.025))
    robot.scoring_mechanism.stop_motor()

    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.4))

    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-366.722, -343.969), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    schedule_function(0.25, robot.scoring_mechanism.intake)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-311.932, -348.762))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-311.932, -393.762))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-311.932, -373.762), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-360.228, -386.703))


def positive_win_point(robot):
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    robot.wall_stake_mechanism.motor.spin_to_position(140, DEGREES, wait=False)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-398.228, -386.703), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-398.228, -406.703), use_back=True)
    robot.wall_stake_mechanism.motor.spin_to_position(-300, DEGREES, wait=False)
    time.sleep(0.25)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-398.228, -386.703))
    robot.wall_stake_mechanism.motor.spin_to_position(300, DEGREES, wait=False)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 30))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-340.377, -317.759), use_back=True)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 70))
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-295.548, -313.837))
    time.sleep(1)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(30, 70))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-367.153, -287.775))


def negative_4_rings_and_touch(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.4))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-407.153, -287.775), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-407.153, -267.775), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-407.153, -272.775))
    robot.scoring_mechanism.intake()
    stop_and_sleep(robot, 0.25)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-407.153, -292.775))
    robot.wall_stake_mechanism.motor.spin_to_position(500, DEGREES, wait=False)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.4))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-349.302, -361.719), use_back=True)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.4))
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-294.511, -366.513))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-294.511, -401.513))
    # robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 500))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-296.248, -391.665), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-286.248, -391.665))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-272.106, -405.807))
    # robot.wall_stake_mechanism.motor.spin_to_position(0, DEGREES, wait=False)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-282.712, -395.2), use_back=True)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.4))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-277.712, -395.2))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-377.712, -395.2), use_back=True)


def positive_2_mobile_goal(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 100))
    robot.mobile_goal_clamp.release_mobile_goal()
    # robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    # robot.wall_stake_mechanism.motor.spin_to_position(200, DEGREES, wait=False)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-367.712, -395.2))
    robot.scoring_mechanism.set_speed(40)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-291.108, -459.479))
    robot.scoring_mechanism.set_speed(0)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 50))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-248.108, -459.479), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 100))
    robot.scoring_mechanism.set_speed(70)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-258.108, -459.479))
    time.sleep(0.35)
    robot.scoring_mechanism.set_speed(0)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-283.108, -459.479))
    robot.mobile_goal_clamp.release_mobile_goal()
    time.sleep(0.5)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 30))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-283.108, -409.479), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-257.396, -378.837))


def win_point_states(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(40, 40))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-207.396, -378.837))
    robot.scoring_mechanism.spin_lower_intake(100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-164.97, -421.264))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-116.97, -421.264), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    schedule_function(0.3, lambda: robot.scoring_mechanism.stop_motor())
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-131.97, -421.264))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-151.97, -421.264))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-151.97, -366.264), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    schedule_function(0.25, lambda: robot.scoring_mechanism.set_speed(100))
    if robot.alliance_color == "red":
        robot.drivetrain.move_to_point(Translation2d.from_centimeters(-197.933, -327.697))
        robot.mobile_goal_clamp.release_mobile_goal()
        robot.corner_mechanism.lower_corner_mechanism()
        robot.drivetrain.move_to_point(Translation2d.from_centimeters(-182.612, -340.552), use_back=True)
        robot.corner_mechanism.raise_corner_mechanism()
        robot.drivetrain.move_to_point(Translation2d.from_centimeters(-205.593, -321.269))


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
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-212.021, -313.608))
    robot.scoring_mechanism.stop_motor()
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOW_SCORING)
    stop_and_sleep(robot, 0.25)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-201.093, -326.631), use_back=True)
    robot.wall_stake_mechanism.transition_to(WallStakeState.DOCKED)
    stop_and_sleep(robot, 0.2)
    robot.scoring_mechanism.set_speed(100)
    schedule_function(0.3, lambda: robot.scoring_mechanism.intake_until_ring() or robot.scoring_mechanism.set_speed(100) or time.sleep(0.25) or robot.scoring_mechanism.intake_until_ring())
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-183.886, -302.056))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-155.207, -261.099))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-172.415, -285.673), use_back=True)
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-105.239, -352.848), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-119.382, -338.706))
    stop_and_sleep(robot, 0.25)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-192.994, -381.206))
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-192.994, -431.206))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-241.203, -488.66))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-196.208, -435.037), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-226.849, -460.748), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-159.235, -442.631))
    # robot.scoring_mechanism.spin_lower_intake(100)
    # schedule_function(0.5, lambda: robot.scoring_mechanism.stop_motor())
    schedule_function(0.2, lambda: robot.scoring_mechanism.intake_until_ring())
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-123.879, -477.986))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-88.879, -477.986), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()


def third_win_point_states(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 2.125))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOADING)
    stop_and_sleep(robot, 0.2)
    robot.scoring_mechanism.set_speed(100)
    schedule_function(0.5, lambda: robot.scoring_mechanism.set_speed(-50))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-95.307, -470.326))
    robot.scoring_mechanism.stop_motor()
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOW_SCORING)
    stop_and_sleep(robot, 0.25)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-84.38, -483.348), use_back=True)
    robot.wall_stake_mechanism.transition_to(WallStakeState.DOCKED)
    robot.scoring_mechanism.set_speed(100)
    schedule_function(0.3, lambda: robot.scoring_mechanism.intake_until_ring() or robot.scoring_mechanism.intake_until_no_ring() or robot.scoring_mechanism.intake_until_ring())
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-67.173, -458.774))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-38.494, -417.816))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-55.701, -442.391), use_back=True)
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(9.413, -497.028), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    stop_and_sleep(robot, 0.5)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(9.413, -502.028))
    robot.scoring_mechanism.set_speed(-100)
    robot.mobile_goal_clamp.release_mobile_goal()
    schedule_function(0.2, robot.scoring_mechanism.intake_until_ring)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(9.413, -552.028))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(52.413, -552.028), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    stop_and_sleep(robot, 0.1)
    robot.scoring_mechanism.spin_upper_intake(100)
    robot.scoring_mechanism.spin_lower_intake(-100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-67.587, -552.028))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-57.587, -552.028), use_back=True)
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-114.156, -608.596))
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 2))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-100.014, -594.454), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-85.872, -580.312), use_back=True)
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOW_SCORING)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-2.703, -461.535))


def negative_full_mobile_goal(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.5))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(57.297, -461.535), use_back=True)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    stop_and_sleep(robot, 0.25)
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(101.222, -428.435))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(61.29, -458.526), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(61.29, -393.526))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(101.29, -393.526))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-3.71, -393.526), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-46.136, -351.099))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-31.994, -365.242), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-53.207, -344.028))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-17.852, -379.384), use_back=True)
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-17.852, -499.384))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(-17.852, -529.384))


def negative_full_mobile_goal_point_based(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(1.5, 1.5))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(60.0, -0.0), use_back=True)
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


def test_autonomous(robot):
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(82.148, -529.384))
    robot.drivetrain.move_to_point(Translation2d.from_centimeters(82.148, -429.384))


def color_sort_test(robot):
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)


available_autos = [new_skills_alliance_stake, win_point_states, third_win_point_states, win_point, negative_4_rings_and_touch, color_sort_test, negative_full_mobile_goal]
