from Constants import *
from Drivetrain import Drivetrain
from VEXLib import Util
from VEXLib.Motor import Motor
from VEXLib.Robot.RobotBase import RobotBase
from VEXLib.Robot.ScrollBufferedScreen import ScrollBufferedScreen
from VEXLib.Sensors.Controller import Controller
from VEXLib.Util import time
from VEXLib.Util.Logging import Logger
from vex import Competition, PRIMARY, FontType, Inertial

main_log = Logger(Brain().sdcard, Brain().screen, MAIN_LOG_FILENAME)
debug_log = Logger(Brain().sdcard, Brain().screen, DEBUG_LOG_FILENAME)


class Robot(RobotBase):
    def __init__(self, brain):
        super().__init__(brain)
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

        self.screen = ScrollBufferedScreen(max_lines=20)
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
        self.on_setup()

    @main_log.logged
    def on_setup(self):
        self.calibrate_sensors()
        self.main_log.info("Setup complete")

        self.drivetrain.measure_properties()

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
