import io
import sys

from VEXLib.Robot.ScrollingScreen import ScrollingScreen
from VEXLib.Util.Buffer import Buffer

from Constants import *
from VEXLib.Subsystems.TankDrivetrain import Drivetrain
from VEXLib import Util
from VEXLib.Geometry.Translation2d import Translation2d
from VEXLib.Motor import Motor
from VEXLib.Network.Telemetry import SerialCommunication
from VEXLib.Robot.RobotBase import RobotBase
from VEXLib.Sensors.Controller import Controller
from VEXLib.Util import time
from VEXLib.Util.Logging import Logger
from vex import Competition, PRIMARY, FontType, Inertial

main_log = Logger(Brain().sdcard, Brain().screen, "main")
debug_log = Logger(Brain().sdcard, Brain().screen, "debug")


class Robot(RobotBase):
    def __init__(self, brain):
        super().__init__(brain)
        self.serial_communication = SerialCommunication("/dev/port19", "/dev/port20")

        self.brain.screen.set_font(FontType.MONO12)
        self.controller = Controller(PRIMARY)

        self.drivetrain = Drivetrain(
            [Motor(Ports.PORT10, GearRatios.DRIVETRAIN, True),
             Motor(Ports.PORT2, GearRatios.DRIVETRAIN, True),
             Motor(Ports.PORT3, GearRatios.DRIVETRAIN, True)],
            [Motor(Ports.PORT9, GearRatios.DRIVETRAIN, False),
             Motor(Ports.PORT5, GearRatios.DRIVETRAIN, False),
             Motor(Ports.PORT8, GearRatios.DRIVETRAIN, False)],
            Inertial(Ports.PORT20),
            self.log_and_print)

        self.screen = ScrollingScreen(Buffer(20))
        self.main_log = main_log
        self.debug_log = debug_log

        self.competition = Competition(self.on_driver_control, self.on_autonomous)

    def log_and_print(self, *parts):
        self.brain.screen.set_font(FontType.MONO15)
        message = " ".join(map(str, parts))
        self.screen.add_line(message)

        for row, line in Util.enumerate(self.screen.get_screen_content()):
            self.brain.screen.set_cursor(row, 1)
            self.brain.screen.clear_row(row)
            self.brain.screen.print(line)

        self.main_log.log(message)
        print(message)

    def start(self):
        try:
            self.on_setup()
        except Exception as e:
            exception_buffer = io.StringIO()
            sys.print_exception(e, exception_buffer)
            self.serial_communication.send(str(exception_buffer.getvalue()))

            for log_entry in exception_buffer.getvalue().split("\n"):
                main_log.fatal(str(log_entry))
            raise e

    def auto_routine(robot):
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

    @main_log.logged
    def on_setup(self):
        # self.calibrate_sensors()
        self.main_log.info("Setup complete")
        # self.auto_routine()

        # self.drivetrain.measure_properties()

        # self.drivetrain.determine_speed_pid_constants()

        # self.drivetrain.verify_speed_pid()

        # self.drivetrain.verify_odometry()

    @debug_log.logged
    def calibrate_sensors(self):
        self.main_log.info("Calibrating sensors")

        # Set initial sensor positions and calibrate mechanisms.
        self.main_log.debug("Calibrating inertial sensor")
        self.drivetrain.odometry.inertial_sensor.calibrate()
        while self.drivetrain.odometry.inertial_sensor.is_calibrating():
            time.sleep_ms(5)
        self.main_log.debug("Calibrated inertial sensor successfully")
