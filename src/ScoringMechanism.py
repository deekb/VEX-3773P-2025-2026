import math

from VEXLib.Math import is_near_continuous
import VEXLib.Util.time as time
from VEXLib.Util.time import wait_until_not
from vex import VOLT, FORWARD, LedStateType, PERCENT, Rotation, DEGREES, Distance, MM, Brain, Color
from Constants import ScoringMechanismProperties


class ScoringMechanism:
    def __init__(self, lower_intake_motor, upper_intake_motor, rotation_sensor: Rotation, optical_sensor, distance_sensor: Distance, screen: Brain.Lcd):
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

    def set_speed(self, speed):
        self.spin_lower_intake(speed)
        self.spin_upper_intake(speed)

    def spin_lower_intake(self, speed):
        self.lower_intake_motor.spin(FORWARD, speed * (12 / 100), VOLT)

    def spin_upper_intake(self, speed):
        self.upper_intake_motor.spin(FORWARD, speed * (12 / 100), VOLT)

    def stop_motor(self):
        self.set_speed(0)

    def intake(self):
        self.set_speed(100)

    def outtake(self):
        self.set_speed(-100)

    def get_ring_color(self):
        if is_near_continuous(220, self.optical_sensor.hue(), 20, 0, 360):
            return "blue"
        elif is_near_continuous(13, self.optical_sensor.hue(), 20, 0, 360):
            return "red"
        else:
            return None

    def ring_is_near(self):
        return self.distance_sensor.object_distance(MM) < ScoringMechanismProperties.RING_DISTANCE

    def intake_until_ring(self):
        self.intake()
        while not self.ring_is_near():
            pass
        self.stop_motor()

    def intake_until_no_ring(self):
        self.intake()
        wait_until_not(lambda: self.ring_is_near(), 100)
        time.sleep(0.25)
        self.stop_motor()
        print(self.get_ring_color())

    def eject_ring(self):
        self.ejecting_ring = True
        self.eject_ring_at_position = math.ceil(self.get_position())

    def sort_ring(self, alliance_color):
        if self.ejecting_ring:
            if self.get_position() > self.eject_ring_at_position:
                self.outtake()
                time.sleep(0.1)
                self.stop_motor()
                time.sleep(0.25)
                self.intake()
                self.ejecting_ring = False
            return

        if self.ring_is_near():
            if self.found_ring:
                return

            ring_color = self.get_ring_color()
            if not ring_color:
                self.screen.clear_screen()
                self.screen.set_fill_color(Color.BLACK)
                self.screen.set_pen_color(Color.BLACK)
                return
            if ring_color == "red":
                self.screen.clear_screen()
                self.screen.set_fill_color(Color.RED)
                self.screen.set_pen_color(Color.RED)
            elif ring_color == "blue":
                self.screen.clear_screen()
                self.screen.set_fill_color(Color.BLUE)
                self.screen.set_pen_color(Color.BLUE)

            self.screen.draw_rectangle(0, 0, 480, 240)

            self.found_ring = True
            if ring_color != alliance_color:
                self.eject_ring()
            print(self.get_ring_color())
        else:
            self.found_ring = False

    def calibrate(self):
        self.spin_upper_intake(40)
        while self.distance_sensor.object_distance(MM) > ScoringMechanismProperties.HOOK_DISTANCE:
            pass
        self.spin_upper_intake(-20)
        time.sleep(0.25)
        self.spin_upper_intake(20)
        while self.distance_sensor.object_distance(MM) > ScoringMechanismProperties.HOOK_DISTANCE:
            pass
        self.rotation_sensor.set_position(ScoringMechanismProperties.CALIBRATION_OFFSET, DEGREES)
        self.stop_motor()
        # self.eject_ring()
        # self.spin_upper_intake(100)

    def get_position(self):
        return self.rotation_sensor.position(DEGREES) / ScoringMechanismProperties.AVERAGE_HALF_ROTATION

    def tick(self, alliance_color):
        self.sort_ring(alliance_color)

    def loop(self, alliance_color):
        while True:
            self.tick(alliance_color)
