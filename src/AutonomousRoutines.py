import WallStakeMechanismV2 as WallStakeMechanism
from WallStakeMechanismV2 import WallStakeState
from Constants import DrivetrainProperties
from VEXLib.Algorithms.TrapezoidProfile import TrapezoidProfile, Constraints
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation1d import Translation1d
from VEXLib.Util import time
from vex import PERCENT, DEGREES, Thread


def schedule_function(delay, callback):
    def function():
        time.sleep(delay)
        callback()

    Thread(function)


def bonk(robot):
    robot.wall_stake_mechanism.transition_to(WallStakeMechanism.WallStakeState.HIGH_SCORING)
    robot.wall_stake_mechanism.transition_to(WallStakeMechanism.WallStakeState.DOCKED)


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


def new_skills_alliance_stake(robot):
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(40, 30))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    time.sleep(0.25)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(32), 0)
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-60), 90)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    time.sleep(0.5)
    robot.scoring_mechanism.set_speed(100)
    schedule_function(0.2, lambda: robot.scoring_mechanism.intake_until_ring())
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(60), 0)
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOADING)
    time.sleep(0.2)
    robot.scoring_mechanism.set_speed(100)
    schedule_function(0.5, lambda: robot.scoring_mechanism.set_speed(-35))
    schedule_function(0.65, lambda: robot.scoring_mechanism.set_speed(100))
    schedule_function(0.75, lambda: robot.scoring_mechanism.set_speed(-35))
    schedule_function(0.76, lambda: robot.scoring_mechanism.stop_motor())
    schedule_function(0.77, lambda: robot.scoring_mechanism.spin_lower_intake(100))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(98), -55)
    schedule_function(0.7, lambda: robot.wall_stake_mechanism.transition_to(WallStakeState.HIGH_SCORING))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(35), -90)
    # robot.wall_stake_mechanism.transition_to(WallStakeState.HIGH_SCORING)
    time.sleep(0.25)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-33), -90)
    robot.scoring_mechanism.set_speed(-100)
    robot.wall_stake_mechanism.transition_to(WallStakeState.DOCKED)
    schedule_function(0.15, lambda: robot.scoring_mechanism.stop_motor())
    schedule_function(0.4, lambda: robot.scoring_mechanism.set_speed(100))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(160), 180)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-45), 180)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-30), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-55), 40)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(40), 40)

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-181), -90)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    time.sleep(0.25)

    robot.scoring_mechanism.set_speed(100)
    schedule_function(0.2, lambda: robot.scoring_mechanism.intake_until_ring())
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(70), 0)
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOADING)
    time.sleep(0.2)
    robot.scoring_mechanism.set_speed(100)
    schedule_function(0.5, lambda: robot.scoring_mechanism.set_speed(-35))
    schedule_function(0.65, lambda: robot.scoring_mechanism.set_speed(100))
    schedule_function(0.75, lambda: robot.scoring_mechanism.set_speed(-35))
    schedule_function(0.76, lambda: robot.scoring_mechanism.stop_motor())
    schedule_function(0.77, lambda: robot.scoring_mechanism.spin_lower_intake(100))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(82), 50)
    schedule_function(0.85, lambda: robot.wall_stake_mechanism.transition_to(WallStakeState.HIGH_SCORING))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(40), 90)
    # robot.wall_stake_mechanism.transition_to(WallStakeState.HIGH_SCORING)
    time.sleep(0.25)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-30), 90)
    robot.scoring_mechanism.set_speed(-100)
    robot.wall_stake_mechanism.transition_to(WallStakeState.DOCKED)
    schedule_function(0.15, lambda: robot.scoring_mechanism.stop_motor())
    schedule_function(0.16, lambda: robot.scoring_mechanism.set_speed(100))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-10), 90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(160), 180)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-40), 180)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), 90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-40), -55)
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(25), -55)
    schedule_function(0.5, lambda: robot.scoring_mechanism.intake_until_ring())
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(200), 0)
    schedule_function(0.5, lambda: robot.scoring_mechanism.spin_lower_intake(100))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(70), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-80), 110)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)


def win_point(robot):
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-40), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(5), -90)
    robot.scoring_mechanism.intake()
    time.sleep(0.25)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), -90)
    robot.scoring_mechanism.stop_motor()

    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(
        Constraints(DrivetrainProperties.MAX_ACHIEVABLE_SPEED.to_inches_per_second() / 3,
                    DrivetrainProperties.MAX_ACHIEVABLE_SPEED.to_inches_per_second() / 3))

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-90), 130)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    schedule_function(0.25, robot.scoring_mechanism.intake)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(45), -5)
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
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 70))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
    robot.wall_stake_mechanism.motor.spin_to_position(140, DEGREES, wait=False)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-38), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), -90)
    robot.wall_stake_mechanism.motor.spin_to_position(-300, DEGREES, wait=False)
    time.sleep(0.25)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), -90)
    robot.wall_stake_mechanism.motor.spin_to_position(500, DEGREES, wait=False)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 30))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-90), 130)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 70))
    robot.mobile_goal_clamp.clamp_mobile_goal()
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(45), -5)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(35), -90)

    # robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(70, 500))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-10), -80)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(10), 0)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), -45)
    # robot.wall_stake_mechanism.motor.spin_to_position(0, DEGREES, wait=False)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-15), -45)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(20, 500))
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
    robot.drivetrain.odometry.zero_rotation = Rotation2d.from_degrees(-130)
    robot.drivetrain.trapezoidal_profile = TrapezoidProfile(Constraints(30, 30))
    robot.mobile_goal_clamp.release_mobile_goal()
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOADING)
    time.sleep(0.2)
    robot.scoring_mechanism.set_speed(100)
    schedule_function(0.5, lambda: robot.scoring_mechanism.set_speed(-50))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(7), 130)
    robot.scoring_mechanism.stop_motor()
    robot.wall_stake_mechanism.transition_to(WallStakeState.LOW_SCORING)
    time.sleep(0.25)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-15), 130)
    robot.wall_stake_mechanism.transition_to(WallStakeState.DOCKED)
    time.sleep(0.2)
    robot.scoring_mechanism.set_speed(100)
    schedule_function(0.3, lambda: robot.scoring_mechanism.intake_until_ring() or robot.scoring_mechanism.set_speed(100) or time.sleep(0.75) or robot.scoring_mechanism.intake_until_ring())
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), 55)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), 55)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-30), 55)
    robot.scoring_mechanism.stop_motor()
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-75), 135)
    robot.mobile_goal_clamp.clamp_mobile_goal()
    time.sleep(0.25)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(90), -150)
    robot.scoring_mechanism.set_speed(100)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(45), -90)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(50), -130)

    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-40), -130)
    schedule_function(0.5, lambda: robot.scoring_mechanism.set_speed(-100))
    schedule_function(0.55, lambda: robot.scoring_mechanism.stop_motor())
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-40), 40)
    robot.mobile_goal_clamp.release_mobile_goal()
    schedule_function(0.2, lambda: robot.scoring_mechanism.intake_until_ring())
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(70), 15)
    # robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-50), 180)
    # robot.mobile_goal_clamp.clamp_mobile_goal()


def test_autonomous(robot):
    robot.drivetrain.odometry.zero_rotation = Rotation2d.from_degrees(45)
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(100), 45+(90*0))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(100), 45+(90*1))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(100), 45+(90*2))
    robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(100), 45+(90*3))


available_autos = [new_skills_alliance_stake, win_point_states, second_win_point_states, positive_2_mobile_goal, test_autonomous, negative,
                   skills_alliance_stake, win_point]
