import time

from Logging import Logger
from VEXLib.Algorithms.TrapezoidProfile import TrapezoidProfile, Constraints

from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation1d import Translation1d
from Constants import DrivetrainProperties
from VEXLib.Geometry.Translation2d import Translation2d

if False:
    from CompetitionRobot import Robot

autonomous_log = Logger("logs/Autonomous")

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
        return Rotation2d.from_degrees(0)


    def execute(self):
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(24), 0)

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


class LongGoalLow(AutonomousRoutine):
    name = "Long Goal Low"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(-90)

    def execute(self):
        self.robot.drivetrain.trapezoidal_profile = TrapezoidProfile(
            Constraints(
                DrivetrainProperties.MAX_ACHIEVABLE_SPEED.to_meters_per_second(),
                DrivetrainProperties.MAX_ACHIEVABLE_SPEED.to_meters_per_second(),
            )
        )
        self.robot.intake.raise_intake()
        self.robot.intake.run_floating_intake(1)
        self.robot.intake.run_upper_intake(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(32), -90)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(5), 180)
        time.sleep(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-10), 180)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-25), 180)
        self.robot.intake.run_intake(1)


class LongGoalHigh(AutonomousRoutine):
    name = "Long Goal High"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(90)

    def execute(self):
        self.robot.drivetrain.trapezoidal_profile = TrapezoidProfile(
            Constraints(
                DrivetrainProperties.MAX_ACHIEVABLE_SPEED.to_meters_per_second(),
                DrivetrainProperties.MAX_ACHIEVABLE_SPEED.to_meters_per_second(),
            )
        )

        self.robot.intake.raise_intake()
        self.robot.intake.run_floating_intake(1)
        self.robot.intake.run_upper_intake(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(30), 90)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(5), 180)
        time.sleep(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-10), 180)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-25), 180)
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
        return Rotation2d.from_degrees(6)

    def pre_match_setup(self):
        self.robot.intake.lower_intake()

    def execute(self):
        self.robot.intake.run_floating_intake(1)
        self.robot.intake.run_upper_intake(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(33), 6)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-7), 128)
        self.robot.intake.run_intake(1)
        time.sleep(0.4)
        self.robot.intake.stop_intake()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(41), 128)
        self.robot.intake.raise_intake()
        self.robot.intake.run_upper_intake(1)
        self.robot.intake.run_floating_intake(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(15), 180)
        time.sleep(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-27), 180)
        self.robot.intake.run_intake(1)


class ElimsHigh(AutonomousRoutine):
    name = "Elims High"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(27)

    def execute(self):
        self.robot.intake.run_floating_intake(1)
        self.robot.intake.run_upper_intake(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(46), 27)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(7), 10)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-8), 10)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(25), -120)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(35), 125)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(10), 0)


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


all_routines = [LongGoalLow, LongGoalHigh, SimpleLow, SimpleHigh, DoNothingAutonomous]
