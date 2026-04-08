

from VEXLib.Math import is_near
from VEXLib.Util.Logging import Logger

from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation1d import Translation1d
from VEXLib.Geometry.Velocity1d import Velocity1d
from TankDrivetrainOld import TimeBasedCommand
import VEXLib.Util.time as time
from Constants import IntakeConstants
from vex import Color, Thread

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
        self.robot.drivetrain.acceleration_scalar = factor

    def set_speed_factor(self, factor):
        self.robot.drivetrain.velocity_scalar = factor

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


class Drive(AutonomousRoutine):
    name = "Drive"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():

        return Rotation2d.from_degrees(180)

    def execute(self):
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(35), 180)



class Right4Long(AutonomousRoutine):
    name = "Right 4 Long" #add hook at the end
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(-90)

    def execute(self):
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(31.5), -90, max_extra_time=0)
        self.robot.match_load_helper.extend()
        self.robot.intake.run_floating_intake(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(10), 180)

        # Pick up #1 from match loader
        time.sleep(0.1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-32), 180, max_extra_time=0, turn_first=False)
        self.robot.match_load_helper.retract()


        self.robot.intake.extend_flap()
        self.robot.intake.set_lever_velocity(100)
        time.sleep(0.5)
        self.robot.intake.retract_flap()
        self.robot.intake.move_lever_to_position(0)
        self.robot.descoring_arm.wing_out_and_down()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(15), 180, turn_first=False)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-15), 125)
        self.set_speed_factor(0.4)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-28), 180)
        self.robot.drivetrain.set_speed(Velocity1d.from_zero(), Velocity1d.from_zero())
        while True:
            self.robot.drivetrain.update_powers()


class Left4Long(AutonomousRoutine):
    name = "Left 4 Long" #Add Hook
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(90)

    def execute(self):
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(31.5), 90, max_extra_time=0)
        self.robot.match_load_helper.extend()
        self.robot.intake.run_floating_intake(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(10), 180)

        # Pick up #1 from match loader
        time.sleep(0.1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-32), 180, max_extra_time=0, turn_first=False)
        self.robot.match_load_helper.retract()


        self.robot.intake.extend_flap()
        self.robot.intake.set_lever_velocity(100)
        time.sleep(0.5)
        self.robot.intake.retract_flap()
        self.robot.intake.move_lever_to_position(0)
        self.robot.descoring_arm.wing_out_and_down()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(15), 180, turn_first=False)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-15), 125)
        self.set_speed_factor(0.4)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-28), 180)
        while True:
            self.robot.drivetrain.update_powers()

class Right6Long(AutonomousRoutine):
    name = "Right 6 Long"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(-12.5)

    def execute(self):
        self.robot.intake.run_floating_intake(1)
        self.set_acceleration_factor(0.6)
        self.set_speed_factor(0.6)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(23), -12.5)
        # self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(5), -12.5)
        self.set_acceleration_factor(1)

        self.robot.match_load_helper.extend()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(28), -120)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(21), -180, max_extra_time=0)
        # Picking up
        self.robot.drivetrain.set_powers(0.1, 0.1)
        self.robot.intake.intake_until_color(bad_color(self.robot), timeout=3)
        self.robot.drivetrain.set_powers(0, 0)
        # self.robot.drivetrain.back_up_to_goal(-0.5)
        # TODO: JANKY ANGLE
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-4), -185, turn_first=False)
        self.robot.intake.retract_flap()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-30), -185, max_extra_time=0)

        self.robot.intake.extend_flap()
        self.robot.intake.set_lever_velocity(30)
        self.robot.intake.run_floating_intake(1)
        start_time = time.time()
        while not is_near(self.robot.intake.get_lever_position(), IntakeConstants.SCORE_POSITION, 5) and (time.time() - start_time < 2):
            time.sleep_ms(5)
        self.robot.intake.stop_floating_intake()
        self.robot.descoring_arm.wing_out_and_down()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(14), 180, turn_first=False)
        self.robot.match_load_helper.retract()
        Thread(lambda: self.robot.intake.move_lever_to_position(0))
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-17), 125)
        self.set_speed_factor(0.4)
        self.robot.intake.run_floating_intake(-1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-23), 182)
        while True:
            self.robot.drivetrain.update_powers()

    def cleanup(self):
        self.robot.intake.retract_flap()
        self.robot.intake.stop_floating_intake()

class Left6Long(AutonomousRoutine):
    name = "Left 6 Long"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(12.5)

    def execute(self):
        self.robot.intake.run_floating_intake(1)
        self.set_acceleration_factor(0.6)
        self.set_speed_factor(0.6)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(23), 12.5)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(5), 12.5)
        self.set_acceleration_factor(1)

        self.robot.match_load_helper.extend()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(27), 120)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(21), 180, max_extra_time=0)
        # Picking up
        self.robot.drivetrain.set_powers(0.1, 0.1)
        self.robot.intake.intake_until_color(bad_color(self.robot), timeout=3)
        self.robot.drivetrain.set_powers(0, 0)
        # self.robot.drivetrain.back_up_to_goal(-0.5)
        # TODO: JANKY ANGLE ON OTHER AUTO
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-4), 180, turn_first=False)
        self.robot.intake.retract_flap()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-30), 180, max_extra_time=0)

        self.robot.intake.extend_flap()
        self.robot.intake.set_lever_velocity(30)
        self.robot.intake.run_floating_intake(1)
        start_time = time.time()
        while not is_near(self.robot.intake.get_lever_position(), IntakeConstants.SCORE_POSITION, 5) and (time.time() - start_time < 2):
            time.sleep_ms(5)
        self.robot.intake.stop_floating_intake()
        self.robot.descoring_arm.wing_out_and_down()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(14), 180, turn_first=False)
        self.robot.match_load_helper.retract()
        Thread(lambda: self.robot.intake.move_lever_to_position(0))
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-17), 125)
        self.set_speed_factor(0.4)
        self.robot.intake.run_floating_intake(-1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-23), 182)
        while True:
            self.robot.drivetrain.update_powers()

    def cleanup(self):
        self.robot.intake.retract_flap()
        self.robot.intake.stop_floating_intake()


class GoalLineTest(AutonomousRoutine):
    name = "Goal Line Test"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(180)

    def pre_match_setup(self):
        pass

    def execute(self):
        self.robot.drivetrain.back_up_to_goal(-0.1)

class Left2Mid5Long(AutonomousRoutine):
    name = "Left 2 Mid 5 Long"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(9)

    def pre_match_setup(self):
        pass

    def execute(self):
        self.robot.intake.run_floating_intake(1)
        self.set_acceleration_factor(0.8)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(37), 9, commands=[TimeBasedCommand(-0.8, lambda: self.robot.match_load_helper.extend())])
        self.set_acceleration_factor(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-7), 9)
        self.robot.intake.lower_intake()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-12.5), 134)
        self.robot.intake.extend_flap()
        self.robot.intake.move_lever_to_position(110)
        self.robot.intake.retract_flap()
        self.robot.intake.move_lever_to_position(0)
        self.set_acceleration_factor(1.4)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(44), 134)
        self.robot.intake.raise_intake()
        self.robot.match_load_helper.extend()
        # LAST EDIT WAS HERE, CHANGED 16in -> 14in
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(14), 180)
        # Pickup from match loader
        self.robot.drivetrain.set_powers(0.1, 0.1)
        self.robot.intake.intake_until_color(bad_color(self.robot), timeout=3)
        self.robot.drivetrain.set_powers(0, 0)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-10), 180, turn_first=False)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-24), 180)
        # Score in Long Goal
        self.robot.intake.extend_flap()
        self.robot.intake.set_lever_velocity(100)
        start_time = time.time()
        while not is_near(self.robot.intake.get_lever_position(), IntakeConstants.SCORE_POSITION, 5) and (time.time() - start_time < 2):
            time.sleep_ms(5)
        self.robot.intake.retract_flap()
        Thread(lambda: self.robot.intake.move_lever_to_position(0))
        self.robot.descoring_arm.wing_out_and_down()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(15), 180)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-16), -225)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-17), 180)
        while True:
            self.robot.drivetrain.set_speed(Velocity1d.from_meters_per_second(0), Velocity1d.from_meters_per_second(0))
            self.robot.drivetrain.update_powers()


class LocalWinPoint(AutonomousRoutine):
    name = "Local Win Point"
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

class Skills(AutonomousRoutine):
    name = "Skills"

    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(90)

    def execute(self):
    #     self.robot.midgoal_hood_actuator.extend()
    #
    #     self.set_acceleration_factor(0.8)
    #     self.robot.intake.run_floating_intake(1)
    #     self.robot.intake.run_upper_intake(1)
    #     self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(38), 9, commands=[TimeBasedCommand(-0.45, lambda: self.robot.match_load_helper.extend())])
    #     self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-6), 9)
    #
    #     self.robot.intake.lower_intake()
    #     time.sleep(0.5)
    #
    #     self.set_acceleration_factor(1)
    #     self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-11), 135, max_extra_time=0)
    #     self.robot.intake.run_hood(1)
    #     time.sleep(1)
    #     self.robot.intake.stop_hood()
    #     self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(36), 135, max_extra_time=0)
    #     self.robot.midgoal_hood_actuator.retract()
    #     self.robot.match_load_helper.extend()
    #     self.robot.intake.raise_intake()
    #     self.robot.drivetrain.arc_movement(Rotation2d.from_degrees(45), Translation1d.from_inches(18), "CCW", 135)
    #     self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(8), 180, max_extra_time=0)
    #


        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(21), 90, max_extra_time=0)
        self.robot.match_load_helper.extend()
        # time.sleep(0.5)
        self.robot.drivetrain.arc_movement(Rotation2d.from_degrees(90), Translation1d.from_inches(9), "CCW", 90, turn_first=False)
        self.robot.intake.pickup()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(7), 180, turn_first=False)

        # Pick up #1 from match loader
        self.robot.drivetrain.set_powers(0.1, 0.1)
        time.sleep(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-14), 180, max_extra_time=0, turn_first=False)
        self.robot.match_load_helper.retract()

        self.robot.drivetrain.arc_movement(Rotation2d.from_degrees(175), Translation1d.from_inches(8), "CW", 180)

        # Ride along left wall
        self.set_acceleration_factor(0.9)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(94), 5)
        self.set_acceleration_factor(1)

        self.robot.drivetrain.arc_movement(Rotation2d.from_degrees(90), Translation1d.from_inches(-11), "CW", 90, max_extra_time=0)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-14), 0, turn_first=False)
        self.robot.intake.run_hood(1)
        time.sleep(1.7)
        self.robot.intake.run_hood(-1)
        time.sleep(0.2)
        self.robot.intake.run_hood(1)
        time.sleep(0.8)
        self.robot.match_load_helper.extend()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(33), 0)
        self.robot.intake.stop_hood()
        self.robot.drivetrain.set_powers(0.2, 0.2)
        time.sleep(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-5), 0, turn_first=False, max_extra_time=0)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-29), -2)
        self.robot.match_load_helper.retract()
        self.robot.intake.run_hood(0.8)
        time.sleep(2.4)
        self.robot.intake.run_hood(-1)
        time.sleep(0.2)
        self.robot.intake.run_hood(0.8)
        time.sleep(1)
        self.robot.intake.stop_hood()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(3), 0, turn_first=False, max_extra_time=0)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-8), 0, turn_first=False, max_extra_time=0)
        # self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(2), 0)
        self.robot.drivetrain.arc_movement(Rotation2d.from_degrees(90), Translation1d.from_inches(11), "CW", 0, max_extra_time=0)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(70), -90, turn_first=False, max_extra_time=1.5)
        self.robot.match_load_helper.extend()
        self.robot.drivetrain.arc_movement(Rotation2d.from_degrees(90), Translation1d.from_inches(11), "CCW", -90, turn_first=False, max_extra_time=0)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(11), 0, turn_first=False, max_extra_time=0)
        self.robot.drivetrain.set_powers(0.1, 0.1)
        time.sleep(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-18), 0, commands=[TimeBasedCommand(0.5, self.robot.match_load_helper.retract)], turn_first=False)
        self.robot.drivetrain.arc_movement(Rotation2d.from_degrees(175), Translation1d.from_inches(8), "CW", 0, max_extra_time=0)

        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(92), -175, turn_first=False)

        self.robot.drivetrain.arc_movement(Rotation2d.from_degrees(90), Translation1d.from_inches(-12), "CW", -90, max_extra_time=0)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-14), 180, turn_first=False)
        self.robot.intake.run_hood(1)
        time.sleep(2)
        self.robot.intake.run_hood(-1)
        time.sleep(0.2)
        self.robot.intake.run_hood(1)
        time.sleep(0.8)
        self.robot.intake.stop_hood()
        self.robot.match_load_helper.extend()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(35), 180)
        self.robot.drivetrain.set_powers(0.1, 0.1)
        time.sleep(1)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-3), 180, turn_first=False)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-27), 180)
        self.robot.match_load_helper.retract()
        self.robot.intake.run_hood(0.8)
        time.sleep(2.5)
        self.robot.intake.run_hood(-1)
        time.sleep(0.2)
        self.robot.intake.run_hood(0.8)
        time.sleep(0.8)
        self.robot.intake.stop_hood()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(3), 180, turn_first=False, max_extra_time=0)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-8), 180, turn_first=False, max_extra_time=0)
        self.robot.intake.run_floating_intake(1)
        self.robot.intake.run_upper_intake(1)
        self.robot.drivetrain.arc_movement(Rotation2d.from_degrees(90), Translation1d.from_inches(35), "CW", 180, max_extra_time=0, commands=[TimeBasedCommand(-0.5, self.robot.match_load_helper.extend)])
        self.set_acceleration_factor(1.3)
        self.robot.intake.run_hood(1)
        self.robot.drivetrain.set_powers(0.5, 0.7)
        time.sleep(0.5)
        # self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(8), 90, turn_first=False, max_extra_time=2, commands=[TimeBasedCommand(-0.25, self.robot.match_load_helper.retract)])
        # time.sleep(1)
        self.robot.match_load_helper.retract()
        # self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(12), 90, turn_first=False)
        self.robot.drivetrain.set_powers(0, 0)


class WorldsWinPoint(AutonomousRoutine):
    name = "Worlds Win Point"

    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(-90)

    def execute(self):
        self.set_acceleration_factor(1.2)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(21), -90, max_extra_time=0)
        self.set_acceleration_factor(1)
        self.robot.match_load_helper.extend()
        # time.sleep(0.5)
        self.robot.drivetrain.arc_movement(arc_angle=Rotation2d.from_degrees(90),
                                           arc_radius=Translation1d.from_inches(9),
                                           direction="CW",
                                           start_direction_degrees=-90,
                                           turn_first=False)
        self.robot.intake.pickup()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(7), 180, turn_first=False)

        # Pick up #1 from match loader
        self.robot.drivetrain.set_powers(0.1, 0.1)
        # time.sleep(0.1)
        self.set_acceleration_factor(1.2)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-32), 180, max_extra_time=0, turn_first=False, commands=[TimeBasedCommand(0.1, self.robot.intake.stop_upper_intake), TimeBasedCommand(-0.5, lambda: self.robot.intake.run_hood(1)), TimeBasedCommand(-0.5, lambda: self.robot.intake.run_upper_intake(1))])
        self.robot.match_load_helper.retract()
        # self.robot.drivetrain.set_powers(-0.1, -0.1)

        self.robot.intake.run_hood(1)
        time.sleep(1)

        self.robot.intake.run_hood(0)
        self.set_acceleration_factor(0.8)
        self.robot.drivetrain.arc_movement(arc_angle=Rotation2d.from_degrees(155),
                                           arc_radius=Translation1d.from_inches(9),
                                           direction="CW",
                                           start_direction_degrees=-185,
                                           turn_first=False)
        self.robot.drivetrain.arc_movement(arc_angle=Rotation2d.from_degrees(60),
                                               arc_radius=Translation1d.from_inches(14),
                                           direction="CCW",
                                           start_direction_degrees=30,
                                           turn_first=False,
                                           commands=[TimeBasedCommand(-0.2, self.robot.match_load_helper.extend)])

        self.set_acceleration_factor(1.3)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(50), 90, max_extra_time=0, commands=[TimeBasedCommand(0, self.robot.match_load_helper.retract), TimeBasedCommand(-0.5, self.robot.match_load_helper.extend)])
        self.set_acceleration_factor(1)
        self.robot.intake.lower_intake()
        self.robot.midgoal_hood_actuator.extend()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-6), 90)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-13), 135)
        self.robot.intake.run_hood(1)
        time.sleep(1)
        self.robot.intake.run_hood(0)
        self.robot.intake.raise_intake()
        self.set_acceleration_factor(1.2)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(45), 135, turn_first=False)
        self.robot.midgoal_hood_actuator.retract()
        self.set_acceleration_factor(2)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-20), 180, commands=[TimeBasedCommand(0, self.robot.match_load_helper.retract), TimeBasedCommand(-0.4, lambda: self.robot.intake.run_hood(1))])
        self.robot.intake.run_hood(1)

class SketchyWorldsWinPoint(AutonomousRoutine):
    name = "Sketchy Worlds Win Point"

    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(-90)

    def execute(self):
        self.set_acceleration_factor(1.2)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(21), -90, max_extra_time=0)
        self.set_acceleration_factor(1)
        self.robot.match_load_helper.extend()
        # time.sleep(0.5)
        self.robot.drivetrain.arc_movement(arc_angle=Rotation2d.from_degrees(90),
                                           arc_radius=Translation1d.from_inches(9),
                                           direction="CW",
                                           start_direction_degrees=-90,
                                           turn_first=False)
        self.robot.intake.pickup()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(9), 180, turn_first=False)

        # Pick up #1 from match loader
        self.robot.drivetrain.set_powers(0.1, 0.1)
        # time.sleep(0.1)
        self.set_acceleration_factor(1.2)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-32), 180, max_extra_time=0, turn_first=False, commands=[TimeBasedCommand(0.1, self.robot.intake.stop_upper_intake), TimeBasedCommand(-0.5, lambda: self.robot.intake.run_hood(1)), TimeBasedCommand(-0.5, lambda: self.robot.intake.run_upper_intake(1))])
        self.robot.match_load_helper.retract()
        # self.robot.drivetrain.set_powers(-0.1, -0.1)

        self.robot.intake.run_hood(1)
        time.sleep(1)

        self.robot.intake.run_hood(0)
        self.set_acceleration_factor(0.8)
        # self.robot.drivetrain.arc_movement(arc_angle=Rotation2d.from_degrees(155),
        #                                    arc_radius=Translation1d.from_inches(9),
        #                                    direction="CW",
        #                                    start_direction_degrees=-185,
        #                                    turn_first=False)
        self.robot.drivetrain.turn_to(Rotation2d.from_degrees(70))
        # self.robot.drivetrain.arc_movement(arc_angle=Rotation2d.from_degrees(60),
        #                                        arc_radius=Translation1d.from_inches(14),
        #                                    direction="CCW",
        #                                    start_direction_degrees=30,
        #                                    turn_first=False,
        #                                    commands=[TimeBasedCommand(-0.2, self.robot.match_load_helper.extend)])

        self.set_acceleration_factor(1.3)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(15), 70, max_extra_time=0, turn_first=False)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(50), 90, commands=[TimeBasedCommand(0, self.robot.match_load_helper.retract), TimeBasedCommand(-0.5, self.robot.match_load_helper.extend)])
        self.set_acceleration_factor(1)
        self.robot.intake.lower_intake()
        self.robot.midgoal_hood_actuator.extend()
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-6), 90)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-11), 135)
        self.robot.intake.run_hood(1)
        time.sleep(1)
        self.robot.intake.run_hood(0)
        self.robot.intake.raise_intake()
        self.set_acceleration_factor(1.2)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(45), 135, turn_first=False)
        self.robot.midgoal_hood_actuator.retract()
        self.set_acceleration_factor(2)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(-20), 180, commands=[TimeBasedCommand(0, self.robot.match_load_helper.retract), TimeBasedCommand(-0.4, lambda: self.robot.intake.run_hood(1))])
        self.robot.intake.run_hood(1)


class ColorTest(AutonomousRoutine):
    name = "Color Test"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(180)

    def execute(self):
        self.robot.intake.run_intake(1)
        self.robot.intake.intake_until_color(bad_color(self.robot))

class Square(AutonomousRoutine):
    name = "Square"
    def __init__(self, robot: Robot):
        super().__init__(robot)

    @staticmethod
    def startup_angle():
        return Rotation2d.from_degrees(180)

    def execute(self):
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(24), 180)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(24), -90)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(24), 0)
        self.robot.drivetrain.move_distance_towards_direction_trap(Translation1d.from_inches(24), 90)




all_routines = [Left6Long, Right6Long, Left4Long, Right4Long, Left2Mid5Long, Drive, Skills, GoalLineTest]
