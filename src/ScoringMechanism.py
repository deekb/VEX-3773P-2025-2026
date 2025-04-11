import math

from VEXLib.Math import is_near_continuous
import VEXLib.Util.time as time
from VEXLib.Util.Logging import Logger
from VEXLib.Util.time import wait_until, wait_until_not
from vex import VOLT, FORWARD, LedStateType, PERCENT, Rotation, DEGREES, Distance, MM, Brain, Color
from Constants import ScoringMechanismProperties

scoring_mechanism_log = Logger(Brain().sdcard, Brain().screen, "scoring_mechanism")


class ScoringMechanism:
    """
    A class to represent the scoring mechanism of a robot.

    Attributes:
        lower_intake_motor (Motor): The motor controlling the lower intake.
        upper_intake_motor (Motor): The motor controlling the upper intake.
        rotation_sensor (Rotation): The sensor to measure rotation.
        optical_sensor (Optical): The sensor to detect ring color.
        distance_sensor (Distance): The sensor to measure distance.
        screen (Brain.Lcd): The screen to display information.
        eject_ring_at_position (int): The position to eject the ring.
        ejecting_ring (bool): Flag to indicate if the ring is being ejected.
        found_ring (bool): Flag to indicate if a ring is found.
    """

    def __init__(self, lower_intake_motor, upper_intake_motor, rotation_sensor: Rotation, optical_sensor, distance_sensor: Distance, screen: Brain.Lcd):
        """
        Constructs an instance of the scoring mechanism object.

        Args:
            lower_intake_motor (Motor): The motor controlling the lower intake.
            upper_intake_motor (Motor): The motor controlling the upper intake.
            rotation_sensor (Rotation): The sensor to measure rotation.
            optical_sensor (Optical): The sensor to detect ring color.
            distance_sensor (Distance): The sensor to measure distance.
            screen (Brain.Lcd): The screen to display information.
        """
        self.lower_intake_motor = lower_intake_motor
        self.upper_intake_motor = upper_intake_motor
        self.screen = screen
        self.optical_sensor = optical_sensor
        self.optical_sensor.set_light_power(100, PERCENT)
        self.optical_sensor.set_light(LedStateType.ON)
        self.distance_sensor = distance_sensor
        self.rotation_sensor = rotation_sensor
        self.eject_ring_at_position = 0
        self.ejecting_ring = False
        self.found_ring = False
        self.log = scoring_mechanism_log

    def set_speed(self, speed):
        """
        Sets the speed of both intake motors.

        Args:
            speed (int): The speed to set for the motors.
        """
        self.log.trace("set_speed: {}".format(speed))
        self.spin_lower_intake(speed)
        self.spin_upper_intake(speed)

    def spin_lower_intake(self, speed):
        """
        Spins the lower intake motor at a given speed.

        Args:
            speed (int): The speed to set for the lower intake motor.
        """
        self.lower_intake_motor.spin(FORWARD, speed * (12 / 100), VOLT)

    def spin_upper_intake(self, speed):
        """
        Spins the upper intake motor at a given speed.

        Args:
            speed (int): The speed to set for the upper intake motor.
        """
        self.upper_intake_motor.spin(FORWARD, speed * (12 / 100), VOLT)

    def stop_motor(self):
        """
        Stops both intake motors.
        """
        self.log.trace("Stopping")
        self.set_speed(0)

    def intake(self):
        """
        Sets both intake motors to intake at full speed.
        """
        self.log.trace("Intaking")
        self.set_speed(100)

    def outtake(self):
        """
        Sets both intake motors to outtake at full speed.
        """
        self.log.trace("Outtaking")
        self.set_speed(-100)

    def back_off(self):
        """
        Sets both intake motors to back off at a reduced speed for a short duration.
        """
        self.log.trace("Backing off")
        self.set_speed(-35)
        time.sleep(0.3)
        self.stop_motor()

    def get_ring_color(self):
        """
        Gets the color of the ring detected by the optical sensor.

        Returns:
            str: The color of the ring ('blue', 'red', or None).
        """
        if is_near_continuous(220, self.optical_sensor.hue(), 20, 0, 360):
            return "blue"
        elif is_near_continuous(13, self.optical_sensor.hue(), 20, 0, 360):
            return "red"
        else:
            return None

    def ring_is_near(self):
        """
        Checks if a ring is near based on the distance sensor.

        Returns:
            bool: True if a ring is near, False otherwise.
        """
        return self.distance_sensor.object_distance(MM) < ScoringMechanismProperties.RING_DISTANCE

    def intake_until_ring(self):
        """
        Intakes until a ring is detected by the distance sensor.
        """
        self.log.trace("intake_until_no_ring")
        self.intake()
        wait_until(self.ring_is_near)
        self.stop_motor()
        self.log.debug("intake_until_ring done, found {} ring".format(self.get_ring_color()))


    def intake_until_no_ring(self):
        """
        Intakes until no ring is detected by the distance sensor.
        """
        self.log.trace("intake_until_no_ring")
        self.intake()
        wait_until_not(lambda: self.ring_is_near(), 100)
        time.sleep(0.25)
        self.stop_motor()
        self.log.debug("intake_until_no_ring done, found {} ring".format(self.get_ring_color()))

    def eject_ring(self):
        """
        Sets the mechanism to eject the ring.
        """
        self.ejecting_ring = True
        self.eject_ring_at_position = math.ceil(self.get_position())
        self.log.debug("current position {}".format(self.get_position()))
        self.log.debug("Will eject ring at position {}".format(self.eject_ring_at_position))

    def show_ring_color(self, color):
        """
        Displays the ring color on the screen.

        Args:
            color (Color): The color to display on the screen.
        """
        self.log.trace("show_ring_color")
        self.screen.clear_screen()
        self.screen.set_fill_color(color)
        self.screen.set_pen_color(color)
        self.screen.draw_rectangle(0, 0, 480, 240)

    def sort_ring(self, alliance_color):
        """
        Sorts the ring based on the alliance color.

        Args:
            alliance_color (str): The color of the alliance ('red' or 'blue').
        """
        # Check if the mechanism is currently ejecting a ring
        if self.ejecting_ring:
            # self.log.debug("state: ejecting_ring")
            # If the current position is greater than the ejection position, outtake the ring
            if self.get_position() > self.eject_ring_at_position:
                self.outtake()
                time.sleep(0.25)
                self.intake()
                self.log.debug("ejecting: current position {}".format(self.get_position()))
                self.ejecting_ring = False
            return

        # Check if a ring is near using the distance sensor
        if self.ring_is_near():
            # If a ring has already been found, do nothing
            if self.found_ring:
                return

            # Get the color of the detected ring
            ring_color = self.get_ring_color()
            if not ring_color:
                self.log.warn("Ring color could not be detected")
                # If no color is detected, show black on the screen
                self.show_ring_color(Color.BLACK)
                return
            if ring_color == "red":
                self.log.debug("Detected red ring")
                # If the ring is red, show red on the screen
                self.show_ring_color(Color.RED)
            elif ring_color == "blue":
                self.log.debug("Detected blue ring")
                # If the ring is blue, show blue on the screen
                self.show_ring_color(Color.BLUE)

            self.found_ring = True
            # If the ring color does not match the alliance color, eject the ring
            if ring_color != alliance_color:
                self.eject_ring()
        else:
            # If no ring is near, reset the found_ring flag
            self.found_ring = False

    def calibrate(self):
        """
        Calibrates the scoring mechanism.
        """
        while self.distance_sensor.object_distance(MM) > ScoringMechanismProperties.HOOK_DISTANCE:
            self.spin_upper_intake(40)
        self.spin_upper_intake(-20)
        time.sleep(0.25)
        while self.distance_sensor.object_distance(MM) > ScoringMechanismProperties.HOOK_DISTANCE:
            self.spin_upper_intake(20)
        self.rotation_sensor.set_position(ScoringMechanismProperties.CALIBRATION_OFFSET, DEGREES)
        self.stop_motor()
        target_end_position = math.ceil(self.get_position()) - 0.3
        while self.get_position() < target_end_position:
            self.spin_upper_intake(100)
        self.spin_upper_intake(-40)
        time.sleep(0.05)
        self.spin_upper_intake(0)

    def get_position(self):
        """
        Gets the current position of the rotation sensor.

        Returns:
            float: The current position of the rotation sensor.
        """
        return self.rotation_sensor.position(DEGREES) / ScoringMechanismProperties.AVERAGE_HALF_ROTATION

    def tick(self, alliance_color):
        """
        Performs a single tick of the scoring mechanism.

        Args:
            alliance_color (str): The color of the alliance ('red' or 'blue').
        """
        self.sort_ring(alliance_color)

    def loop(self, alliance_color):
        """
        Continuously performs ticks of the scoring mechanism.

        Args:
            alliance_color (str): The color of the alliance ('red' or 'blue').
        """
        while True:
            self.tick(alliance_color)
