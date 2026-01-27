import time

from Logging import Logger
from VEXLib.Algorithms.TrapezoidProfile import TrapezoidProfile, Constraints
import math

from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation1d import Translation1d
from Constants import DrivetrainProperties
from VEXLib.Geometry.Translation2d import Translation2d
from VEXLib.Subsystems.TankDrivetrain import TimeBasedCommand
from vex import Color

if False:
    from CompetitionRobot import Robot

autonomous_log = Logger("logs/Autonomous")

def bad_color(robot):
    if robot.alliance_color == Color.RED:
        return Color.BLUE
    else:
        return Color.RED

class AutonomousRoutine:
    name = "AutonomousRoutine"
    def __init__(self, robot: Robot):
        self.robot = robot

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(0)

    def pre_match_setup(self):
        pass

    def execute(self):
        return False

    def set_acceleration_factor(self, factor):
        self.robot.drivetrain.trapezoidal_profile.constraints.max_acceleration = DrivetrainProperties.MAX_ACHIEVABLE_SPEED.to_meters_per_second() * factor

    def run_intake_and_raise_descorer(self, speed):
        self.robot.intake.run_intake(speed)
        self.robot.descoring_arm.extend()

    def run_upper_intake_and_raise_descorer(self, speed):
        self.robot.intake.run_upper_intake(speed)
        self.robot.descoring_arm.extend()

    def shake(self, iterations):
        self.robot.drivetrain.set_powers(0.3, 0.3)
        time.sleep(0.2)
        for _ in range(iterations):
            self.robot.drivetrain.set_powers(0.3, 0.3)
            time.sleep(0.2)
            self.robot.drivetrain.set_powers(-0.3, -0.3)
            time.sleep(0.1)
        self.robot.drivetrain.set_powers(0, 0)

    def cleanup(self):
        self.robot.drivetrain.init()
        self.robot.drivetrain.set_powers(0, 0)
        self.robot.flush_all_logs()


class DoNothingAutonomous(AutonomousRoutine):
    name = "DoNothingAutonomous"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    def execute(self):
        return False


class Skills(AutonomousRoutine):
    name = "Skills"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(90)

    def execute(self):
        self.set_acceleration_factor(1)
        self.robot.intake.raise_intake()
        self.robot.descoring_arm.extend()
        self.robot.match_load_helper.extend()
        self.robot.intake.run_upper_intake(1)
        self.robot.intake.run_floating_intake(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(
            Translation1d.from_inches(30), 90
        )
        self.set_acceleration_factor(1.4)

        self.robot.drivetrain.move_distance_towards_direction_trap(
            Translation1d.from_inches(11), 180, max_extra_time=0
        )
        self.set_acceleration_factor(1)

        self.robot.drivetrain.set_powers(0.2, 0.2)
        self.shake(6)
        # time.sleep(2.8)
        time.sleep(0.4)

        self.robot.match_load_helper.retract()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-10), 180)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(20), 45)
        # self.set_acceleration_factor(1.2)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(70), 10)
        # self.set_acceleration_factor(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(13), -90)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-16), 0)
        self.robot.intake.run_intake(-1)
        time.sleep(0.2)
        self.robot.intake.run_intake(1)
        time.sleep(2.8)

        self.robot.intake.run_hood(-0.15)
        self.robot.match_load_helper.extend()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(32), -1)

        self.robot.drivetrain.set_powers(0.2, 0.2)
        self.shake(5)
        # time.sleep(2.8)
        time.sleep(0.4)

        self.robot.match_load_helper.retract()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-32), 0, max_extra_time=0)
        self.robot.intake.run_intake(-1)
        time.sleep(0.2)
        self.robot.intake.run_intake(1)
        time.sleep(2.8)
        self.robot.intake.stop_intake()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(15), 0)
        # self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(26), 0)
        # self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-95), 22)
        # self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-55), 60)
        # self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(10), 120)
        # self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(40), 95)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(92), -90)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-24), 0)
        self.robot.match_load_helper.extend()
        self.robot.intake.run_intake(1)
        time.sleep(0.5)
        self.robot.intake.stop_hood()
        self.robot.intake.run_upper_intake(1)
        self.robot.intake.run_floating_intake(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(32), 0)
        self.robot.drivetrain.set_powers(0.2, 0.2)
        self.shake(5)
        # time.sleep(2.8)
        time.sleep(0.4)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-32), 0)
        self.robot.match_load_helper.retract()
        self.robot.intake.run_intake(-1)
        time.sleep(0.2)
        self.robot.intake.run_intake(1)
        time.sleep(2)
        self.robot.intake.stop_hood()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(12), 0)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(15), -120)
        # self.set_acceleration_factor(1.2)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(70), -170)
        # self.set_acceleration_factor(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(13), 90)
        self.robot.match_load_helper.extend()
        self.robot.intake.run_intake(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(22), 180)
        self.robot.drivetrain.set_powers(0.2, 0.2)
        self.shake(6)
        # time.sleep(2.8)
        time.sleep(0.6)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-8), 180)
        self.robot.match_load_helper.retract()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(20), 125)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(40), 100)


class DriveForwardOneTile(AutonomousRoutine):
    name = "DriveForwardOneTile"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(0)

    def execute(self):
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(24), 0)

class DriveInASquare(AutonomousRoutine):
    name = "DriveInASquare"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(0)

    def execute(self):
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(24), 0)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(24), 90)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(24), 180)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(24), -90)

class DriveInACircle(AutonomousRoutine):
    name = "DriveInACircle"

    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(180)

    def execute(self):
        self.robot.drivetrain.arc_movement(Rotation2d.from_degrees(180), Translation1d.from_inches(-12), "CCW", 180)
        # self.robot.drivetrain.arc_movement(Rotation2d.from_degrees(180), Translation1d.from_inches(12), "CCW", 180)


class SMove(AutonomousRoutine):
    name = "SMove"

    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(180)

    def execute(self):
        self.robot.drivetrain.arc_movement(Rotation2d.from_degrees(180), Translation1d.from_inches(12), "CW", 180, dont_stop=True, max_extra_time=0)
        self.robot.drivetrain.arc_movement(Rotation2d.from_degrees(180), Translation1d.from_inches(12), "CCW", 0, dont_start=True, turn_first=False)
        self.robot.drivetrain.move_until_distance_away(Rotation2d.from_degrees(180), Translation1d.from_inches(12))


class LongGoalLow(AutonomousRoutine):
    name = "Long Goal Low"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(-90)

    def execute(self):
        self.set_acceleration_factor(1.2)

        self.robot.intake.raise_intake()
        self.robot.match_load_helper.extend()
        self.robot.intake.run_floating_intake(0.5)
        self.robot.intake.run_upper_intake(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(31), -90)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(12), 180, max_extra_time=0)
        self.shake(2)
        self.robot.match_load_helper.retract()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-27), 180, max_extra_time=0)
        self.robot.intake.run_intake(1)


class LongGoalHigh(AutonomousRoutine):
    name = "Long Goal High"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(90)

    def execute(self):
        self.set_acceleration_factor(1.2)

        self.robot.intake.raise_intake()
        self.robot.match_load_helper.extend()
        self.robot.intake.run_floating_intake(0.5)
        self.robot.intake.run_upper_intake(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(31), 90)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(12), -180, max_extra_time=0)
        self.shake(2)
        self.robot.match_load_helper.retract()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-27), -180, max_extra_time=0)

        self.robot.intake.run_intake(1)


class SimpleLow(AutonomousRoutine):
    name = "Simple Low"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(-6)

    def execute(self):
        self.robot.intake.run_floating_intake(1)
        self.robot.intake.run_upper_intake(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(33), -6)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(10), 52)
        self.robot.intake.run_upper_intake(-1)
        self.robot.intake.run_floating_intake(-1)
        time.sleep(1.2)
        self.robot.intake.stop_intake()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-41), 52)
        self.robot.intake.run_upper_intake(1)
        self.robot.intake.run_floating_intake(1)
        self.robot.match_load_helper.extend()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(15), 175)
        time.sleep(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-24), 175)
        self.robot.intake.run_intake(1)


class SimpleHigh(AutonomousRoutine):
    name = "Simple High"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(9)

    def pre_match_setup(self):
        pass

    def execute(self):
        self.robot.intake.run_floating_intake(1)
        self.robot.intake.run_upper_intake(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(36), 9, commands=[TimeBasedCommand(-0.35, lambda: self.robot.match_load_helper.extend())])
        # self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(20), 9)
        # self.set_acceleration_factor(0.8)
        # self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(15), 9)
        self.set_acceleration_factor(1.2)
        self.robot.intake.lower_intake()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-5.5), 9)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-11), 134)
        self.robot.intake.run_intake(1)
        time.sleep(0.4)
        # self.robot.intake.run_hood(-1)
        self.set_acceleration_factor(1.4)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(45), 135, commands=[TimeBasedCommand(0.2, lambda:self.robot.intake.run_hood(-1))])
        self.robot.intake.raise_intake()
        self.robot.intake.run_upper_intake(1)
        self.robot.intake.run_floating_intake(1)
        self.robot.match_load_helper.extend()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(14), 180)
        self.robot.drivetrain.set_powers(0.3, 0.3)
        # self.shake(3)
        time.sleep(1)
        # self.robot.match_load_helper.retract()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-32), 180)
        self.robot.intake.run_intake(1)
        time.sleep(3)
        self.robot.intake.stop_intake()
        # self.robot.intake.intake_until_color(bad_color(self.robot), 1, 3)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(17), 180)
        self.robot.descoring_arm.retract()
        self.robot.match_load_helper.retract()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-15), -135)
        self.set_acceleration_factor(0.8)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-25), 180)


class ElimsHigh(AutonomousRoutine):
    name = "Elims High"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(9)

    def execute(self):
        self.set_acceleration_factor(1.2)
        self.robot.descoring_arm.extend()
        self.robot.intake.run_floating_intake(1)
        self.robot.intake.run_upper_intake(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(36), 9, commands=[TimeBasedCommand(-0.375, lambda: self.robot.match_load_helper.extend())])

        # self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(21), -9)
        # self.set_acceleration_factor(0.8)
        # self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(15), -9)
        # self.set_acceleration_factor(1.2)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(32), 135)
        self.robot.match_load_helper.extend()
        # self.set_acceleration_factor(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(21), 180, max_extra_time=0)
        self.robot.drivetrain.set_powers(0.3, 0.3)
        # self.shake(3)
        time.sleep(1)
        # self.robot.match_load_helper.retract()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-33), 180, max_extra_time=0)
        self.robot.intake.run_upper_intake(-1)
        time.sleep(0.15)
        self.robot.intake.run_intake(1)
        time.sleep(2)
        self.robot.intake.stop_intake()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(15), 180)
        self.robot.descoring_arm.retract()
        self.robot.match_load_helper.retract()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-14), -135)
        # self.set_acceleration_factor(1.2)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-25), 180)


class ElimsLow(AutonomousRoutine):
    name = "Elims Low"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(-9)

    def execute(self):
        self.set_acceleration_factor(1.2)
        self.robot.descoring_arm.extend()
        self.robot.intake.run_floating_intake(1)
        self.robot.intake.run_upper_intake(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(36), -9, commands=[TimeBasedCommand(-0.375, lambda: self.robot.match_load_helper.extend())])

        # self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(21), -9)
        # self.set_acceleration_factor(0.8)
        # self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(15), -9)
        # self.set_acceleration_factor(1.2)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(32), -135)
        self.robot.match_load_helper.extend()
        # self.set_acceleration_factor(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(20), 180, max_extra_time=0)
        self.robot.drivetrain.set_powers(0.3, 0.3)
        # self.shake(3)
        time.sleep(1)
        # self.robot.match_load_helper.retract()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-32), 180, max_extra_time=0)
        self.robot.intake.run_upper_intake(-1)
        time.sleep(0.15)
        self.robot.intake.run_intake(1)
        time.sleep(2)
        self.robot.intake.stop_intake()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(15), 180)
        self.robot.descoring_arm.retract()
        self.robot.match_load_helper.retract()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-14), -135)
        # self.set_acceleration_factor(1.2)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-25), 180)


class TurnTest(AutonomousRoutine):
    name = "TurnTest"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(0)

    def execute(self):
        autonomous_log.info("Starting TurnTest")

        for angle in [0, 90, 180, -90, 90, 0]:
            self.robot.drivetrain.turn_to(Rotation2d.from_degrees(angle))
            autonomous_log.info("Turned to {} degrees".format(angle))

        autonomous_log.info("Done TurnTest")
        autonomous_log.flush_logs()


class WinPoint(AutonomousRoutine):
    name = "Win Point"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(-90)

    def execute(self):
        self.set_acceleration_factor(1)
        self.set_acceleration_factor(1.3)

        self.robot.match_load_helper.extend()
        self.robot.intake.raise_intake()

        self.robot.intake.run_floating_intake(1)
        self.robot.intake.run_upper_intake(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(30), -90)
        self.robot.drivetrain.turn_to(Rotation2d.from_degrees(180))
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(10), 180, max_extra_time=0)

        self.robot.drivetrain.set_powers(0.2, 0.2)
        self.shake(1)
        # time.sleep(2.8)
        time.sleep(0.4)

        self.robot.match_load_helper.retract()

        self.set_acceleration_factor(1.6)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-30), 180, max_extra_time=0, commands=[TimeBasedCommand(-0.2, lambda: self.robot.intake.run_intake(1))], turn_first=False)
        self.set_acceleration_factor(1.3)

        time.sleep(1)
        # self.robot.intake.run_hood(-0.25)
        # self.robot.intake.run_upper_intake(-0.5)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(10), 180)
        # self.robot.intake.run_upper_intake(1)
        self.robot.intake.stop_hood()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(64), 77)
        self.set_acceleration_factor(0.9)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(9), 77, turn_first=False)
        self.set_acceleration_factor(1)
        # time.sleep(0.2)
        self.robot.intake.lower_intake()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-12), 132, commands=[TimeBasedCommand(-0.3, lambda: self.robot.intake.run_intake(1))])
        self.set_acceleration_factor(1.3)

        # self.robot.intake.run_intake(1)
        time.sleep(0.7)
        self.robot.intake.run_hood(-1)
        self.robot.intake.raise_intake()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(45), 135)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-20), 180, commands=[TimeBasedCommand(-0.3, lambda: self.robot.intake.run_intake(1))])
        self.robot.intake.run_intake(1)
        # self.robot.brain.screen.draw_rectangle(1, 1, 50, 50, Color.GREEN)

class SkillsArcTurn(AutonomousRoutine):
    name = "Skills Arc Turn"

    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(90)

    def execute(self):
        self.set_acceleration_factor(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(19), 90, dont_stop=True)
        self.robot.match_load_helper.extend()
        self.robot.drivetrain.arc_movement(Rotation2d.from_degrees(90), Translation1d.from_inches(10), "CCW", 90, dont_stop=True, max_extra_time=0)
        self.robot.intake.pickup()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(3), 180, max_extra_time=0)

        # Pick up #1 from match loader
        time.sleep(3)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-14), 180)
        self.robot.match_load_helper.retract()

        self.robot.drivetrain.arc_movement(Rotation2d.from_degrees(180), Translation1d.from_inches(8), "CW", 180, dont_stop=True, max_extra_time=0)

        # Ride along left wall
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(94), 5)

        self.robot.drivetrain.arc_movement(Rotation2d.from_degrees(90), Translation1d.from_inches(-16), "CW", 90, dont_stop=True, max_extra_time=0)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-6), 0)
        self.robot.intake.run_hood(1)
        time.sleep(3)

        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(35), 0, commands=[TimeBasedCommand(0.5, self.robot.match_load_helper.extend)])
        self.robot.intake.stop_hood()
        time.sleep(3)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-35), 0, commands=[TimeBasedCommand(0.5, self.robot.match_load_helper.retract)])
        self.robot.intake.run_hood(1)
        time.sleep(3)
        self.robot.intake.stop_hood()
        self.robot.drivetrain.arc_movement(Rotation2d.from_degrees(0), Translation1d.from_inches(16), "CW", 90, dont_stop=True, max_extra_time=0)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(60), -90, dont_stop=True, max_extra_time=0)
        self.robot.drivetrain.arc_movement(Rotation2d.from_degrees(-90), Translation1d.from_inches(18), "CCW", 90, dont_stop=True, max_extra_time=0, commands=[TimeBasedCommand(0.5, self.robot.match_load_helper.extend)])
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(4), 0, max_extra_time=0)
        time.sleep(3)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-18), 0, commands=[TimeBasedCommand(0.5, self.robot.match_load_helper.retract)])
        self.robot.drivetrain.arc_movement(Rotation2d.from_degrees(0), Translation1d.from_inches(8), "CW", 180, dont_stop=True, max_extra_time=0)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(90), -175)
        self.robot.drivetrain.arc_movement(Rotation2d.from_degrees(-90), Translation1d.from_inches(-16), "CW", 180, dont_stop=True, max_extra_time=0)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-4), 180)
        self.robot.intake.run_hood(1)
        time.sleep(3)
        self.robot.intake.stop_hood()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(30), 180, commands=[TimeBasedCommand(0.5, self.robot.match_load_helper.extend)])
        time.sleep(3)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-30), 180, commands=[TimeBasedCommand(0.5, self.robot.match_load_helper.retract)])
        self.robot.intake.run_hood(1)
        time.sleep(3)
        self.robot.intake.stop_hood()
        self.robot.drivetrain.arc_movement(Rotation2d.from_degrees(180), Translation1d.from_inches(30), "CW", 90, dont_stop=True, max_extra_time=0)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(15), 90)


# all_routines = [Skills, WinPoint, LongGoalLow, LongGoalHigh, SimpleLow, SimpleHigh, DoNothingAutonomous, ElimsLow]
all_routines = [SkillsArcTurn, DriveInACircle, Skills, WinPoint, LongGoalLow, LongGoalHigh, SimpleHigh, ElimsLow, ElimsHigh, DoNothingAutonomous, SMove]
