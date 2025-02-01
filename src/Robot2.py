import json
import VEXLib.Math.MathUtil as MathUtil
import VEXLib.Sensors.Controller
import AutonomousRoutines2 as AutonomousRoutines
from ConstantsV2 import *
from CornerMechanism import CornerMechanism
from DrivetrainV2 import Drivetrain
from MobileGoalClamp import MobileGoalClamp
from ScoringMechanism import ScoringMechanism
from VEXLib.Kinematics import desaturate_wheel_speeds
from VEXLib.Robot.RobotBase import RobotBase
from VEXLib.Robot.ScrollBufferedScreen import ScrollBufferedScreen
from VEXLib.Util import time, pass_function
from VEXLib.Util.Logging import Logger
from WallStakeMechanismV2 import WallStakeMechanism
from vex import *


def ramp_voltage_and_collect_data(motor_group, step_delay=0.25, voltage_step=0.1, max_voltage=12):
    """
    Ramp the voltage from 0 to the maximum voltage and collect torque, power, and efficiency data.

    :param step_delay: Time (in seconds) to wait between each voltage step.
    :param voltage_step: Incremental voltage step (in volts).
    :param max_voltage: Maximum allowable voltage (in volts).
    :return: A JSON string with torque-voltage, power-voltage, and efficiency-voltage data.
    """
    data = {
        "voltage": [],
        "torque": [],
        "speed": [],
        "power": [],
        "efficiency": []
    }

    print("Starting voltage ramp and data collection...")

    for voltage in [i * voltage_step for i in range(int(max_voltage / voltage_step) + 1)]:
        # Apply the current voltage to the motors
        [motor.spin(FORWARD, voltage, VOLT) for motor in motor_group]
        total_torque = total_speed = total_power = total_efficiency = 0
        # Wait for the drivetrain to respond
        time.sleep(step_delay)
        for _ in range(10):
            total_torque += sum([motor.torque(TorqueUnits.NM) for motor in motor_group])
            total_speed += sum([motor.velocity(PERCENT) for motor in motor_group])  # in radians/sec
            total_power += sum([motor.power(PowerUnits.WATT) for motor in motor_group])
            total_efficiency += sum([motor.efficiency(PERCENT) for motor in motor_group])
            time.sleep(0.1)

        average_torque = total_torque / (10 * len(motor_group))
        average_speed = total_speed / (10 * len(motor_group))
        average_power = total_power / (10 * len(motor_group))
        average_efficiency = total_efficiency / (10 * len(motor_group))

        # Append data to the lists
        data["voltage"].append(voltage)
        data["torque"].append(average_torque)
        data["speed"].append(total_speed / (10 * len(motor_group)))
        data["power"].append(total_power / (10 * len(motor_group)))
        data["efficiency"].append(total_efficiency / (10 * len(motor_group)))

        print("Voltage: {:.2f}V, Speed: {:.2f}%, Torque: {:.2f}Nm, Power: {:.2f}W, Efficiency: {:.2f}".format(
            voltage, total_speed / (10 * len(motor_group)), total_torque / (10 * len(motor_group)),
                     total_power / (10 * len(motor_group)), total_efficiency / (10 * len(motor_group))))

    # Stop the drivetrain
    [motor.spin(FORWARD, 0, VOLT) for motor in motor_group]

    # Convert the data to JSON format
    json_data = json.dumps(data)
    return json_data


# noinspection DuplicatedCode
class Robot(RobotBase):
    def __init__(self, brain):
        super().__init__(brain)
        self.controller = VEXLib.Sensors.Controller.Controller(PRIMARY)
        self.drivetrain = Drivetrain([Motor(Ports.PORT14, GearRatios.DRIVETRAIN, True),
                                      Motor(Ports.PORT13, GearRatios.DRIVETRAIN, True),
                                      Motor(Ports.PORT12, GearRatios.DRIVETRAIN, False)],

                                     [Motor(Ports.PORT15, GearRatios.DRIVETRAIN, False),
                                      Motor(Ports.PORT16, GearRatios.DRIVETRAIN, False),
                                      Motor(Ports.PORT17, GearRatios.DRIVETRAIN, True)])

        self.screen = ScrollBufferedScreen()

        self.main_log = Logger(self.brain.sdcard, MAIN_LOG_FILENAME)

        self.alliance_color = None

        self.mobile_goal_clamp = MobileGoalClamp(ThreeWirePorts.MOBILE_GOAL_CLAMP_PISTON)
        self.corner_mechanism = CornerMechanism(DigitalOut(ThreeWirePorts.DOINKER_PISTON))
        self.scoring_mechanism = ScoringMechanism(
            [Motor(Ports.PORT1, GearSetting.RATIO_18_1, False),
             Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)],
            Rotation(Ports.PORT18),
            Optical(Ports.PORT10),
            Distance(Ports.PORT5))
        self.wall_stake_mechanism = WallStakeMechanism(Motor(Ports.PORT8, GearSetting.RATIO_18_1, False),
                                                       Rotation(Ports.PORT21))

        self.user_preferences = DefaultPreferences
        self.autonomous_mappings = {str(function)[10:]: function for function in AutonomousRoutines.available_autos}
        print([dir(function) for function in AutonomousRoutines.available_autos])
        self.autonomous = pass_function
        self.competition = Competition(self.on_driver_control, self.on_autonomous)

    def log_and_print(self, *parts):
        message = " ".join(map(str, parts))
        self.screen.add_line(message)
        self.brain.screen.clear_screen()
        self.brain.screen.set_cursor(1, 1)
        for line in self.screen.get_screen_content():
            self.brain.screen.print(line)
            self.brain.screen.next_row()
        self.main_log.log(message)
        print(message)

    def debug_wait(self):
        while not self.controller.buttonA.pressing():
            pass
        while self.controller.buttonA.pressing():
            pass

    def on_autonomous(self):
        self.drivetrain.reset()
        self.log_and_print("Executing chosen autonomous routine:", str(self.autonomous))
        self.autonomous(self)

    def get_selection(self, options):
        """
        Allows the user to navigate through a list of options and select one using specified controls.
        The function implements a loop to display and navigate through options using a controller.
        It reacts to button presses to modify the selection index or make a selection.

        Args:
            options (list): A list of options from which the user can select.

        Returns:
            Any: The selected option from the list.
        """
        selection_index = 0

        while True:
            self.controller.screen.clear_screen()
            self.controller.screen.set_cursor(1, 1)
            self.controller.screen.print(options[selection_index])
            while not (
                    self.controller.buttonRight.pressing() or self.controller.buttonLeft.pressing() or self.controller.buttonA.pressing()):
                time.sleep_ms(5)

            if self.controller.buttonA.pressing():
                break

            if self.controller.buttonRight.pressing():
                selection_index += 1
            elif self.controller.buttonLeft.pressing():
                selection_index -= 1

            while self.controller.buttonRight.pressing() or self.controller.buttonLeft.pressing():
                time.sleep_ms(5)

            if selection_index < 0:
                selection_index = 0
            elif selection_index >= len(options) - 1:
                selection_index = len(options) - 1
        while self.controller.buttonA.pressing():
            time.sleep_ms(5)

        return options[selection_index]

    def select_autonomous_routine(self):
        self.log_and_print("Starting autonomous routine selection")
        autonomous_type = self.get_selection(["red", "blue", "skills_alliance_stake"])
        self.alliance_color = {"red": "red", "blue": "blue", "skills_alliance_stake": ""}[autonomous_type]

        if autonomous_type == "skills_alliance_stake":
            self.drivetrain.set_angles_inverted(False)
            self.autonomous = self.autonomous_mappings[autonomous_type]
            self.log_and_print("Skills routine chosen:", autonomous_type)
            return autonomous_type

        auto = self.get_selection(list(self.autonomous_mappings.keys()))

        self.drivetrain.set_angles_inverted(autonomous_type == "blue")
        self.autonomous = self.autonomous_mappings[auto]

        return autonomous_type + " " + auto

    def start(self):
        self.on_setup()

    def on_setup(self):
        self.wall_stake_mechanism.rotation_sensor.set_position(-100, DEGREES)
        self.drivetrain.odometry.inertial_sensor.calibrate()
        self.log_and_print("Calibrating inertial sensor...")
        while self.drivetrain.odometry.inertial_sensor.is_calibrating():
            time.sleep_ms(5)
        self.log_and_print("Calibrated inertial sensor successfully")
        self.controller.rumble("..")
        self.log_and_print("Selecting autonomous routine...")
        autonomous_routine = self.select_autonomous_routine()
        self.log_and_print("Selected autonomous routine:", autonomous_routine)

        drive_style = self.get_selection(["Dirk", "Derek"])
        self.log_and_print("Selected drive style:", drive_style)

        if drive_style == "Dirk":
            self.user_preferences = DirkPreferences
            self.setup_dirk_preferences()
        elif drive_style == "Derek":
            self.user_preferences = DerekPreferences
            self.setup_derek_preferences()

        self.log_and_print("Set up user preferences:", drive_style)

        self.log_and_print("Setup complete")
        # self.log_and_print("Measuring drivetrain properties...")
        # self.log_and_print("Left drivetrain properties:", ramp_voltage_and_collect_data(self.drivetrain.left_motors))
        # self.log_and_print("Right drivetrain properties:", ramp_voltage_and_collect_data(self.drivetrain.right_motors))

    def on_driver_control(self):
        self.drivetrain.reset()
        while True:
            self.driver_control_periodic()
            time.sleep_ms(20)

    def driver_control_periodic(self):
        left_speed = right_speed = 0
        if self.user_preferences.CONTROLLER_BINDINGS_STYLE == ControlStyles.TANK:
            left_speed = self.controller.left_stick_y()
            right_speed = self.controller.right_stick_y()

            left_speed = MathUtil.apply_deadband(left_speed)
            right_speed = MathUtil.apply_deadband(right_speed)
        elif self.user_preferences.CONTROLLER_BINDINGS_STYLE in [ControlStyles.ARCADE, ControlStyles.SPLIT_ARCADE]:
            forward_speed = turn_speed = 0
            forward_speed = self.controller.left_stick_y()
            if self.user_preferences.CONTROLLER_BINDINGS_STYLE == ControlStyles.ARCADE:
                turn_speed = self.controller.left_stick_x()
            elif self.user_preferences.CONTROLLER_BINDINGS_STYLE == ControlStyles.SPLIT_ARCADE:
                turn_speed = self.controller.right_stick_x()

            forward_speed = MathUtil.apply_deadband(forward_speed)
            turn_speed = -MathUtil.apply_deadband(turn_speed)

            left_speed = forward_speed - turn_speed
            right_speed = forward_speed + turn_speed
        else:
            self.log_and_print("Invalid controller bindings style:", self.user_preferences.CONTROLLER_BINDINGS_STYLE)

        left_speed, right_speed = desaturate_wheel_speeds([left_speed, right_speed])

        left_speed = MathUtil.clamp(left_speed, -1, 1)
        right_speed = MathUtil.clamp(right_speed, -1, 1)

        left_speed = MathUtil.cubic_filter(left_speed, linearity=self.user_preferences.CUBIC_FILTER_LINEARITY)
        right_speed = MathUtil.cubic_filter(right_speed, linearity=self.user_preferences.CUBIC_FILTER_LINEARITY)

        # self.log_and_print("Updating drivetrain voltages - Left:", left_speed, "Right:", right_speed)
        self.drivetrain.set_voltage(left_speed * self.user_preferences.MAX_MOTOR_VOLTAGE,
                                    right_speed * self.user_preferences.MAX_MOTOR_VOLTAGE)

        self.drivetrain.update_odometry()
        self.wall_stake_mechanism.tick()
        # self.scoring_mechanism.tick(self.alliance_color)

    def setup_dirk_preferences(self):
        """Setup controller buttons for DirkPreferences."""
        self.log_and_print("Setting up Dirk Preferences")
        self.controller.buttonB.pressed(
            lambda: self.log_and_print("Toggling clamp") or self.mobile_goal_clamp.toggle_clamp())
        self.controller.buttonL2.pressed(self.scoring_mechanism.outtake)
        self.controller.buttonL2.released(self.scoring_mechanism.stop_motor)
        self.controller.buttonR2.pressed(self.scoring_mechanism.intake)
        self.controller.buttonR1.pressed(self.wall_stake_mechanism.next_state)
        self.controller.buttonL1.pressed(self.wall_stake_mechanism.previous_state)

        self.controller.buttonR2.released(lambda: self.scoring_mechanism.spin_motor_at_speed(-35) or time.sleep(0.05) or self.scoring_mechanism.stop_motor())

        self.controller.buttonY.pressed(self.corner_mechanism.toggle_corner_mechanism)
        self.controller.buttonRight.pressed(self.scoring_mechanism.intake_until_ring)

    def setup_derek_preferences(self):
        """Setup controller buttons for DerekPreferences."""
        self.log_and_print("Setting up Derek Preferences")
        self.controller.buttonUp.pressed(lambda: self.drivetrain.turn_to_gyro(0))
        self.controller.buttonLeft.pressed(lambda: self.drivetrain.turn_to_gyro(90))
        self.controller.buttonDown.pressed(lambda: self.drivetrain.turn_to_gyro(180))
        self.controller.buttonRight.pressed(lambda: self.drivetrain.turn_to_gyro(270))
        self.controller.buttonB.pressed(lambda: self.log_and_print("Toggling clamp") or self.mobile_goal_clamp.toggle_clamp())
        self.controller.buttonL1.pressed(self.scoring_mechanism.intake)
        self.controller.buttonL1.released(self.scoring_mechanism.stop_motor)
        self.controller.buttonL2.pressed(self.scoring_mechanism.outtake)
        self.controller.buttonL2.released(lambda: self.scoring_mechanism.spin_motor_at_speed(-35) or time.sleep(0.3) or self.scoring_mechanism.stop_motor())

        self.controller.buttonR1.pressed(self.wall_stake_mechanism.next_state)
        self.controller.buttonR2.pressed(self.wall_stake_mechanism.previous_state)

        self.controller.buttonY.pressed(lambda: self.log_and_print("Toggling corner mechanism") or self.corner_mechanism.toggle_corner_mechanism())
